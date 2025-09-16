from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from .models import WireManufacturingProcess, ManufacturingProcessAction
from .workflow import WIRE_WORKFLOW
from apps.users.models import QcUserModel

class ManufacturingWorkflowService:
    def __init__(self, user: QcUserModel):
        """
        Initializes the service with the request user.
        """
        self.user = user
        self.workflow_config = WIRE_WORKFLOW
        self.stages_order = list(self.workflow_config.keys())

    def start_process(self):
        """Starts a new master manufacturing process."""
        process = WireManufacturingProcess.objects.create(
            stage=self.stages_order[0], # Start at the first stage
            current_step=1,
            created_by=self.user
        )
        self._log_action(process, 'start', process.stage, 0, process.stage, 1, "Process started.")
        return process

    def approve_or_reject_step(self, process_id: int, action: str, comment: str = None):
        """Processes an 'approve' or 'reject' action on the master workflow."""
        process = self._get_process(process_id)
        if process.is_completed:
            raise ValidationError("This process is already complete.")

        stage_config = self.workflow_config.get(process.stage)
        step_config = self._get_step_config(stage_config, process.current_step)
        
        self._check_permission(step_config)

        from_stage, from_step = process.stage, process.current_step
        
        if action == 'approve':
            self._handle_approval(process, stage_config)
        elif action == 'reject':
            self._handle_rejection(process, step_config, comment)
        else:
            raise ValidationError("Invalid action.")

        process.save()
        self._log_action(process, action, from_stage, from_step, process.stage, process.current_step, comment)
        
        if action == 'reject':
            process.is_rejected = False
            process.save(update_fields=['is_rejected'])

        return process

    def _get_process(self, process_id):
        try:
            return WireManufacturingProcess.objects.get(pk=process_id)
        except WireManufacturingProcess.DoesNotExist:
            raise ValidationError(f"Process with ID {process_id} not found.")

    def _get_step_config(self, stage_config, step_number):
        step_config = next((s for s in stage_config.get('steps', []) if s['step'] == step_number), None)
        if not step_config:
            raise ValidationError(f"Configuration for step {step_number} not found.")
        return step_config

    def _check_permission(self, step_config):
        required_group = step_config.get('actor_permission')
        if not self.user.groups.filter(name=required_group).exists() and not self.user.is_superuser:
            raise PermissionDenied(f"Required group: '{required_group}'.")

    def _handle_approval(self, process, stage_config):
        next_step_number = process.current_step + 1
        is_last_step = not any(s['step'] == next_step_number for s in stage_config['steps'])

        if is_last_step:
            self._transition_to_next_stage(process)
        else:
            process.current_step = next_step_number

    def _transition_to_next_stage(self, process):
        current_stage_index = self.stages_order.index(process.stage)
        if current_stage_index + 1 < len(self.stages_order):
            process.stage = self.stages_order[current_stage_index + 1]
            process.current_step = 1
        else:
            process.is_completed = True

    def _handle_rejection(self, process, step_config, comment):
        on_reject = step_config.get('on_reject')
        if not on_reject:
            raise ValidationError("This step cannot be rejected.")
        if not comment:
            raise ValidationError(on_reject.get('message', "A rejection reason is required."))
        process.current_step = on_reject['go_to_step']
        process.is_rejected = True

    def _log_action(self, process, action_type, from_stage, from_step, to_stage, to_step, comment):
        ManufacturingProcessAction.objects.create(
            process=process, user=self.user, action_type=action_type,
            from_stage=from_stage, from_step=from_step,
            to_stage=to_stage, to_step=to_step, comment=comment
        )
        
    def delete_process(self, process_id: int):
        """Hard deletes a master process and its log."""
        process = self._get_process(process_id)
        process.delete()

