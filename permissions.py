# apps/wire/permissions.py
from rest_framework.permissions import BasePermission
from .models import WireManufacturingProcess, DeviceRawMaterial, DeviceChecklist, DeviceProduction, DeviceProduct
from .workflow import WIRE_WORKFLOW

class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class WireObjectPermissionBase(BasePermission):
    """
    Base permission class to find the workflow associated with a given object.
    """
    def get_workflow_request(self, obj):
        """Finds the active master workflow process for a given form object."""
        # For DeviceRawMaterial, the link is now a direct ForeignKey
        if isinstance(obj, DeviceRawMaterial):
            return obj.manufacturing_process
            
        try:
            # For other models, find the process via the OneToOneField
            query_filter = {f"{obj._meta.model_name}__pk": obj.pk}
            return WireManufacturingProcess.objects.get(**query_filter)
        except WireManufacturingProcess.DoesNotExist:
            return None

    def get_step_config(self, workflow_request):
        """Gets the configuration for the current step from workflow.py."""
        if not workflow_request or workflow_request.is_completed:
            return None
        stage_config = WIRE_WORKFLOW.get(workflow_request.stage)
        if not stage_config:
            return None
        return next((step for step in stage_config['steps'] if step['step'] == workflow_request.current_step), None)

    def has_group_permission(self, user, required_group):
        """Checks if a user is in the required group or is a superuser."""
        if not required_group:
            return False
        return user.groups.filter(name=required_group).exists() or user.is_superuser

class CanCreateFormForStage(BasePermission):
    """
    Checks if a user can CREATE a form for a specific stage.
    - The workflow must be in the correct stage.
    - The corresponding form link on the workflow must be empty (except for raw materials).
    - The user must belong to the group authorized for the CURRENT step of that stage.
    - Special Rule: Only QC can create rawmaterial and license forms.
    """
    def has_permission(self, request, view):
        workflow_id = request.data.get('workflow_id')
        if not workflow_id:
            self.message = "A 'workflow_id' is required to create this form."
            return False

        try:
            process = WireManufacturingProcess.objects.get(pk=workflow_id)
        except WireManufacturingProcess.DoesNotExist:
            self.message = f"Workflow with ID {workflow_id} not found."
            return False

        model_name = view.queryset.model._meta.model_name
        
        stage_to_field_map = {
            'devicerawmaterial': ('rawmaterial', 'raw_material'),
            'deviceauthorization': ('license', 'authorization'),
            'devicechecklist': ('checklist', 'checklist'),
            'deviceproduction': ('production', 'production'),
            'deviceproduct': ('product', 'product_final'),
        }
        
        stage_name, model_field = stage_to_field_map.get(model_name, (None, None))
        view.stage_name = model_field  # Pass field name to the view for linking

        if not stage_name:
            self.message = "Internal configuration error: This form is not part of the master workflow."
            return False
        
        # Special rule for initial forms
        if stage_name in ['rawmaterial', 'license'] and not request.user.groups.filter(name='QC').exists() and not request.user.is_superuser:
            self.message = "Only users in the 'QC' group can create Raw Material and Authorization forms."
            return False

        if process.stage != stage_name:
             self.message = f"Workflow is currently in stage '{process.stage}', not '{stage_name}'. Cannot create form."
             return False

        # This check is now skipped for devicerawmaterial to allow multiple instances.
        if model_name != 'devicerawmaterial':
            if hasattr(process, model_field) and getattr(process, model_field) is not None:
                self.message = f"A {model_name} form has already been created for this workflow."
                return False
            
        stage_config = WIRE_WORKFLOW.get(process.stage, {})
        step_config = next((s for s in stage_config.get('steps', []) if s['step'] == process.current_step), None)

        if not step_config:
             self.message = "Workflow step configuration not found."
             return False
        
        required_group = step_config.get('actor_permission')
        if not request.user.groups.filter(name=required_group).exists() and not request.user.is_superuser:
            self.message = f"You are not in the required group ('{required_group}') to create this form for the current step."
            return False

        return True

class CanUpdateFormForStage(WireObjectPermissionBase):
    """
    Handles granular, field-level permissions for UPDATING forms based on the workflow state.
    """
    def has_object_permission(self, request, view, obj):
        process = self.get_workflow_request(obj)
        if not process or process.is_completed:
            return request.user.is_superuser # Only superuser can edit after completion

        step_config = self.get_step_config(process)
        if not step_config:
            return False
        
        required_group = step_config.get('actor_permission')
        if not self.has_group_permission(request.user, required_group):
            self.message = f"Your group is not authorized to perform actions at this step."
            return False

        # --- Granular Field-Level Security Logic ---
        user_group_name = request.user.groups.first().name if request.user.groups.exists() else None
        incoming_data = request.data.keys()
        action_details = step_config.get('details', {})

        # CHECKLIST STAGE
        if isinstance(obj, DeviceChecklist):
            if user_group_name == 'QC':
                # QC can edit anything EXCEPT operator_approval in the nested tests
                if 'qc_tests_wire' in incoming_data:
                    for test_data in request.data.get('qc_tests_wire', []):
                        if 'operator_approval' in test_data:
                            self.message = "QC users cannot change the 'operator_approval' field."
                            return False
            elif user_group_name == 'OP':
                # Operator can ONLY edit operator_approval in nested tests
                allowed_keys = {'qc_tests_wire'}
                if not set(incoming_data).issubset(allowed_keys):
                    self.message = "Operators can only modify 'qc_tests_wire' data."
                    return False
                for test_data in request.data.get('qc_tests_wire', []):
                    allowed_nested_keys = {'id', 'operator_approval'}
                    if not set(test_data.keys()).issubset(allowed_nested_keys):
                        self.message = "Operators can only submit 'id' and 'operator_approval' for a test."
                        return False

        # PRODUCTION STAGE
        elif isinstance(obj, DeviceProduction):
            action = step_config.get('action')
            if user_group_name == 'QC' and action == "Fill out 'FormSpecifications' for production.":
                allowed = {'document_code', 'license_number', 'trace_date', 'trace_code', 'description'}
                if not set(incoming_data).issubset(allowed):
                    self.message = "At this step, QC can only fill out Form Specification fields."
                    return False
            elif user_group_name == 'OP' and action == "Fill production data fields.":
                allowed = {'production'}
                allowed_nested = set(action_details.get('fields', [])) | {'id'}
                if not set(incoming_data).issubset(allowed):
                    self.message = "At this step, Operators can only submit production data."
                    return False
                for prod_item in request.data.get('production', []):
                    if not set(prod_item.keys()).issubset(allowed_nested):
                        self.message = f"Invalid fields submitted for production data. Allowed: {list(allowed_nested)}"
                        return False
            # Add other production stage rules here...

        # PRODUCT STAGE
        elif isinstance(obj, DeviceProduct):
            if user_group_name != 'QC' and not request.user.is_superuser:
                self.message = "Only QC users can create or edit the final product form."
                return False
                
        return True

