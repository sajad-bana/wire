# apps/wire/views.py
from rest_framework import viewsets, mixins, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError


# Correctly and explicitly import all necessary models from their specific files
from .models import (
    DeviceRawMaterial, DeviceAuthorization, DeviceChecklist, DeviceProduction, DeviceProduct,
    WireManufacturingProcess
)
# Import lookup models from their specific location
from .dir_classes.wire_abstract_class import (
    UnsharedFieldStructure, QcTestWireDefinition, Material, CoatingMaterial, WireFormName
)

from .serializers import (
    UnsharedFieldStructureSerializer, QcTestWireDefinitionSerializer,
    MaterialSerializer, CoatingMaterialSerializer, WireFormNameSerializer,
    DeviceRawMaterialSerializer, DeviceAuthorizationSerializer, DeviceChecklistSerializer,
    DeviceProductionSerializer, DeviceProductSerializer, WireManufacturingProcessSerializer,
    FormExtruderSettingsSerializer, FormFiberWeaverSettingsSerializer, FormRadiantSettingsSerializer, FormShieldWeaverSettingsSerializer
)
from .pagination import CustomPagination
from .services import ManufacturingWorkflowService
from .permissions import IsSuperUser, CanCreateFormForStage, CanUpdateFormForStage

# --- Lookups ViewSets (Restored) ---
###
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

# @extend_schema(tags=['Wire - Lookups'])
# class UnsharedFieldStructureViewSet(viewsets.ModelViewSet):
#     queryset = UnsharedFieldStructure.objects.order_by('pk').all()
#     serializer_class = UnsharedFieldStructureSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = CustomPagination
@extend_schema(tags=['Wire - Lookups'])
class UnsharedFieldStructureViewSet(viewsets.ModelViewSet):
    queryset = UnsharedFieldStructure.objects.order_by('pk').all()
    serializer_class = UnsharedFieldStructureSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @extend_schema(
        summary="List all unshared field structures",
        examples=[
            OpenApiExample(
                'List Response',
                description='Paginated list of unshared field structures',
                value={
                    "count": 2,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": 1,
                            "name": "Extruder Structure",
                            "structure": {
                                "temperature_zones": ["zone1", "zone2", "zone3"],
                                "pressure_settings": ["low", "medium", "high"]
                            }
                        },
                        {
                            "id": 2,
                            "name": "Radiant Structure", 
                            "structure": {
                                "wrap_settings": ["tight", "loose"],
                                "strip_configurations": ["standard", "custom"]
                            }
                        }
                    ]
                }
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new unshared field structure",
        examples=[
            OpenApiExample(
                'Create Structure',
                description='Create a new field structure template',
                value={
                    "name": "Custom Structure",
                    "structure": {
                        "custom_fields": ["field1", "field2"],
                        "validation_rules": ["required", "numeric"]
                    }
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

@extend_schema(tags=['Wire - Lookups'])
class QcTestWireDefinitionViewSet(viewsets.ModelViewSet):
    queryset = QcTestWireDefinition.objects.order_by('pk').all()
    serializer_class = QcTestWireDefinitionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

@extend_schema(tags=['Wire - Lookups'])
class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.order_by('pk').all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

@extend_schema(tags=['Wire - Lookups'])
class CoatingMaterialViewSet(viewsets.ModelViewSet):
    queryset = CoatingMaterial.objects.order_by('pk').all()
    serializer_class = CoatingMaterialSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

# @extend_schema(tags=['Wire - Lookups'])
# class WireFormNameViewSet(viewsets.ModelViewSet):
#     queryset = WireFormName.objects.order_by('pk').all()
#     serializer_class = WireFormNameSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = CustomPagination
@extend_schema(tags=['Wire - Lookups'])
class WireFormNameViewSet(viewsets.ModelViewSet):
    queryset = WireFormName.objects.order_by('pk').all()
    serializer_class = WireFormNameSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @extend_schema(
        summary="List all wire form names",
        examples=[
            OpenApiExample(
                'List Response',
                value={
                    "count": 4,
                    "results": [
                        {"id": 1, "name": "Extruder", "type_form": "Authorizations"},
                        {"id": 2, "name": "Radiant", "type_form": "Authorizations"},
                        {"id": 3, "name": "ShieldWeaver", "type_form": "Authorizations"},
                        {"id": 4, "name": "FiberWeaver", "type_form": "Authorizations"}
                    ]
                }
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new wire form name",
        examples=[
            OpenApiExample(
                'Create Form Name',
                value={
                    "name": "NewDevice",
                    "type_form": "Productions"
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


# --- Form ViewSets with Workflow Permissions ---

# class BaseWorkflowViewSet(viewsets.ModelViewSet):
#     """
#     Base ViewSet for forms that are part of the master workflow.
#     It links form creation/updates to the master process.
#     """
#     pagination_class = CustomPagination
    
#     def get_permissions(self):
#         if self.action == 'create':
#             self.permission_classes = [CanCreateFormForStage]
#         elif self.action in ['update', 'partial_update']:
#             self.permission_classes = [CanUpdateFormForStage]
#         else:
#             self.permission_classes = [IsAuthenticated]
#         return super().get_permissions()

#     # The conflicting create method has been removed. 
#     # The default behavior from ModelViewSet will now be used, 
#     # which correctly calls the custom create method in the serializer.
class BaseWorkflowViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet for forms that are part of the master workflow.
    It links form creation/updates to the master process.
    """
    pagination_class = CustomPagination
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [CanCreateFormForStage]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [CanUpdateFormForStage]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def handle_exception(self, exc):
        """
        Handle exceptions and provide meaningful error messages.
        """
        if isinstance(exc, ValidationError):
            return Response(
                {"detail": "Validation error", "errors": exc.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif isinstance(exc, PermissionDenied):
            return Response(
                {"detail": "Permission denied", "message": str(exc)},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)

# @extend_schema(tags=['Wire - Forms'])
# class DeviceRawMaterialViewSet(BaseWorkflowViewSet):
#     queryset = DeviceRawMaterial.objects.all()
#     serializer_class = DeviceRawMaterialSerializer
#     pagination_class = CustomPagination
@extend_schema(tags=['Wire - Forms'])
class DeviceRawMaterialViewSet(BaseWorkflowViewSet):
    queryset = DeviceRawMaterial.objects.all()
    serializer_class = DeviceRawMaterialSerializer
    pagination_class = CustomPagination

    @extend_schema(
        summary="Create a new raw material form",
        examples=[
            OpenApiExample(
                'Create Raw Material',
                description='Create a raw material form with QC tests',
                value={
                    "workflow_id": 1,
                    "form_name": 1,
                    "document_code": "RM-2025-001",
                    "license_number": "LIC-RM-001",
                    "trace_date": "2025-09-16",
                    "trace_code": "TRACE-RM-001",
                    "description": "High grade aluminum wire",
                    "product": 1,
                    "customer": 1,
                    "qc_tests_wire": [
                        {
                            "test_definition": 1,
                            "test_result": True,
                            "operator_approval": True,
                            "quality_control_approval": True,
                            "description": "Conductivity test passed"
                        }
                    ]
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update a raw material form",
        examples=[
            OpenApiExample(
                'Update Raw Material',
                value={
                    "description": "Updated description",
                    "qc_tests_wire": [
                        {
                            "id": 1,
                            "operator_approval": False,
                            "description": "Needs retest"
                        }
                    ]
                }
            )
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


###
from django.contrib.contenttypes.models import ContentType
from .dir_classes.device_settings import (
    FormExtruderSettings, FormRadiantSettings, 
    FormFiberWeaverSettings, FormShieldWeaverSettings
)
@extend_schema(tags=['Wire - Forms'])
class DeviceAuthorizationViewSet(BaseWorkflowViewSet):
    queryset = DeviceAuthorization.objects.all()
    serializer_class = DeviceAuthorizationSerializer
    pagination_class = CustomPagination

    
    @extend_schema(
        examples=[
            OpenApiExample(
                'Complete Authorization Example',
                summary='Full DeviceAuthorization with all nested data',
                description='Complete example with proper field mapping.',
                value={
                    "workflow_id": 1,
                    "form_name_id": 1,
                    "document_code": "AUTH-2025-005",
                    "license_number": "LIC-FULL-123",
                    "trace_date": "2025-09-16",
                    "trace_code": "TRACE-FULL-456",
                    "description": "Complete authorization example",
                    "product_id": 1,
                    "customer_id": 1,
                    "unshared_fields_id": 1,
                    "device_settings": {
                        "insulation_thickness": 2.5,
                        "wire_outer_diameter": 3.2,
                        "preheater_temperature": 180.0,
                        "linear_speed": 15.5,
                        "tensile_force": 120.0
                    },
                    "license_production": {
                        "setup_license_number": "SETUP-FULL-789",
                        "order_number": "PO-2025-104",
                        "total_order_amount": [{"length": 2000, "strand": 4}],
                        "required_amount": [{"length": 1980, "strand": 4}]
                    },
                    "packaging": {
                        "packaging_type": "Steel Reel",
                        "packaging_quantity": "10 units",
                        "packaging_size": "Large"
                    },
                    "raw_material_specifications": [
                        {
                            "raw_material_type": "Aluminum",
                            "raw_material_amount": "800kg",
                            "product_code": "AL-99.7"
                        }
                    ]
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Save the DeviceAuthorization instance
        authorization = serializer.save()

        # Get form_name and settings data
        form_name = None
        if authorization.form_name:
            form_name = authorization.form_name.name
        elif 'form_name_id' in self.request.data:
            try:
                from .dir_classes.wire_abstract_class import WireFormName
                form_name_obj = WireFormName.objects.get(id=self.request.data['form_name_id'])
                form_name = form_name_obj.name
            except WireFormName.DoesNotExist:
                pass

        settings_data = self.request.data.get('device_settings', {})

        if not settings_data or not form_name:
            return

        settings_instance = None
        try:
            # Create the appropriate settings model
            if form_name == 'Extruder':
                settings_serializer = FormExtruderSettingsSerializer(data=settings_data)
                if settings_serializer.is_valid(raise_exception=True):
                    settings_instance = settings_serializer.save(authorization=authorization)
                    
            elif form_name == 'Radiant':
                settings_serializer = FormRadiantSettingsSerializer(data=settings_data)
                if settings_serializer.is_valid(raise_exception=True):
                    settings_instance = settings_serializer.save(authorization=authorization)
                    
            elif form_name == 'FiberWeaver':
                settings_serializer = FormFiberWeaverSettingsSerializer(data=settings_data)
                if settings_serializer.is_valid(raise_exception=True):
                    settings_instance = settings_serializer.save(authorization=authorization)
                    
            elif form_name == 'ShieldWeaver':
                settings_serializer = FormShieldWeaverSettingsSerializer(data=settings_data)
                if settings_serializer.is_valid(raise_exception=True):
                    settings_instance = settings_serializer.save(authorization=authorization)

            # Set up the GenericForeignKey relationship
            if settings_instance:
                content_type = ContentType.objects.get_for_model(settings_instance)
                authorization.settings_content_type = content_type
                authorization.settings_object_id = settings_instance.id
                authorization.save()
                
        except ValidationError as e:
            # Clean up authorization if settings creation fails
            authorization.delete()
            raise e
        except Exception as e:
            authorization.delete()
            raise ValidationError(f"Failed to create device settings: {str(e)}")
    
    def handle_exception(self, exc):
        """Enhanced error handling for authorization creation."""
        if isinstance(exc, ValidationError):
            error_detail = {}
            if hasattr(exc, 'detail'):
                error_detail = exc.detail
            return Response({
                "detail": "Validation failed",
                "errors": error_detail,
                "help": "Check that product_id, customer_id, form_name_id, and unshared_fields_id reference valid objects"
            }, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)
# @extend_schema(tags=['Wire - Forms'])
# class DeviceChecklistViewSet(BaseWorkflowViewSet):
#     queryset = DeviceChecklist.objects.all()
#     serializer_class = DeviceChecklistSerializer
#     pagination_class = CustomPagination
@extend_schema(tags=['Wire - Forms'])
class DeviceChecklistViewSet(BaseWorkflowViewSet):
    queryset = DeviceChecklist.objects.all()
    serializer_class = DeviceChecklistSerializer
    pagination_class = CustomPagination

    @extend_schema(
        summary="Create a device checklist",
        examples=[
            OpenApiExample(
                'Create Checklist',
                value={
                    "workflow_id": 1,
                    "form_name": 1,
                    "document_code": "CHK-2025-001",
                    "trace_date": "2025-09-16",
                    "trace_code": "TRACE-CHK-001",
                    "product": 1,
                    "customer": 1,
                    "work_shift": "shift1",
                    "amount_test_samples": "10 samples",
                    "qc_tests_wire": [
                        {
                            "test_definition": 1,
                            "test_result": True,
                            "operator_approval": True,
                            "quality_control_approval": True,
                            "description": "Pre-production checklist passed"
                        }
                    ]
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

# @extend_schema(tags=['Wire - Forms'])
# class DeviceProductionViewSet(BaseWorkflowViewSet):
#     queryset = DeviceProduction.objects.all()
#     serializer_class = DeviceProductionSerializer
#     pagination_class = CustomPagination
@extend_schema(tags=['Wire - Forms'])
class DeviceProductionViewSet(BaseWorkflowViewSet):
    queryset = DeviceProduction.objects.all()
    serializer_class = DeviceProductionSerializer
    pagination_class = CustomPagination

    @extend_schema(
        summary="Create a production form",
        examples=[
            OpenApiExample(
                'Create Production',
                value={
                    "workflow_id": 1,
                    "form_name": 1,
                    "document_code": "PROD-2025-001",
                    "trace_date": "2025-09-16",
                    "trace_code": "TRACE-PROD-001",
                    "product": 1,
                    "production": [
                        {
                            "operator_name": "John Smith",
                            "start_date": "2025-09-16",
                            "end_date": "2025-09-17",
                            "input_spool_length": "1000m",
                            "input_spool_number": "SP-001",
                            "output_spool_length": "950m",
                            "output_spool_number": "SP-OUT-001",
                            "operator_approval": True,
                            "quality_control_approval": False,
                            "description": "Initial production run"
                        }
                    ],
                    "production_wastes": [
                        {
                            "waste_type": "Conductor waste",
                            "waste_amount": "50m"
                        }
                    ]
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

# @extend_schema(tags=['Wire - Forms'])
# class DeviceProductViewSet(BaseWorkflowViewSet):
#     queryset = DeviceProduct.objects.all()
#     serializer_class = DeviceProductSerializer
#     pagination_class = CustomPagination
@extend_schema(tags=['Wire - Forms'])
class DeviceProductViewSet(BaseWorkflowViewSet):
    queryset = DeviceProduct.objects.all()
    serializer_class = DeviceProductSerializer
    pagination_class = CustomPagination

    @extend_schema(
        summary="Create a final product form",
        examples=[
            OpenApiExample(
                'Create Product',
                value={
                    "workflow_id": 1,
                    "form_name": 1,
                    "document_code": "PROD-FINAL-2025-001",
                    "trace_date": "2025-09-16",
                    "trace_code": "TRACE-FINAL-001",
                    "product": 1,
                    "up_meter": "1000",
                    "down_meter": "950",
                    "color": "Blue",
                    "size": "2.5mm",
                    "net_weight": "45.5kg",
                    "gross_weight": "47.2kg"
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

# --- Master Workflow API Views (Refactored to simple APIViews) ---

@extend_schema(tags=['Wire - Master Workflow'])
class StartManufacturingProcessView(APIView):
    """Starts a new master manufacturing process."""
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Start a new master manufacturing process", request=None, responses={201: WireManufacturingProcessSerializer})
    def post(self, request, *args, **kwargs):
        service = ManufacturingWorkflowService(user=request.user)
        process = service.start_process()
        serializer = WireManufacturingProcessSerializer(process)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(tags=['Wire - Master Workflow'])
class ManufacturingProcessDetailView(APIView):
    """Retrieve or delete a master manufacturing process."""
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsSuperUser()]
        return super().get_permissions()

    @extend_schema(summary="Get the status of a specific manufacturing process", responses={200: WireManufacturingProcessSerializer})
    def get(self, request, pk, *args, **kwargs):
        try:
            process = WireManufacturingProcess.objects.get(pk=pk)
            serializer = WireManufacturingProcessSerializer(process)
            return Response(serializer.data)
        except WireManufacturingProcess.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(summary="Delete a master process (Superuser only)")
    def delete(self, request, pk, *args, **kwargs):
        service = ManufacturingWorkflowService(user=request.user)
        try:
            service.delete_process(process_id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)


class PerformActionPayloadSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    comment = serializers.CharField(required=False, allow_blank=True)

# @extend_schema(tags=['Wire - Master Workflow'])
# class PerformProcessActionView(APIView):
#     """Approve or reject a step in the master workflow."""
#     permission_classes = [IsAuthenticated]

#     @extend_schema(summary="Approve or reject a step in the master workflow", request=PerformActionPayloadSerializer, responses={200: WireManufacturingProcessSerializer})
#     def post(self, request, pk, *args, **kwargs):
#         serializer = PerformActionPayloadSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         service = ManufacturingWorkflowService(user=request.user)
#         try:
#             updated_process = service.approve_or_reject_step(
#                 process_id=pk,
#                 **serializer.validated_data
#             )
#             response_serializer = WireManufacturingProcessSerializer(updated_process)
#             return Response(response_serializer.data)
#         except (ValidationError, PermissionDenied) as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except WireManufacturingProcess.DoesNotExist:
#             return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
@extend_schema(tags=['Wire - Master Workflow'])
class PerformProcessActionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Approve or reject a step in the master workflow",
        request=PerformActionPayloadSerializer,
        responses={200: WireManufacturingProcessSerializer},
        examples=[
            OpenApiExample(
                'Approve Step',
                description='Approve the current step to move workflow forward',
                value={
                    "action": "approve",
                    "comment": "Quality checks passed, approving for next stage"
                }
            ),
            OpenApiExample(
                'Reject Step',
                description='Reject the current step with reason',
                value={
                    "action": "reject", 
                    "comment": "Material quality does not meet specifications, returning for revision"
                }
            )
        ]
    )
    def post(self, request, pk, *args, **kwargs):
        serializer = PerformActionPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service = ManufacturingWorkflowService(user=request.user)
        try:
            updated_process = service.approve_or_reject_step(
                process_id=pk,
                **serializer.validated_data
            )
            response_serializer = WireManufacturingProcessSerializer(updated_process)
            return Response(response_serializer.data)
        except (ValidationError, PermissionDenied) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except WireManufacturingProcess.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)