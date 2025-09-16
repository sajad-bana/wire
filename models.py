# apps/wire/models.py

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.users.models import QcUserModel

from .dir_classes.wire_device_rawmaterial import *
from .dir_classes.wire_license_production import *
from .dir_classes.wire_device_checklist import *
from .dir_classes.wire_device_production import *

from .dir_classes.production_qc_settings import *

from apps.marketing.models import Product


# --- Master Workflow Models --------------------------------------------------

class WireManufacturingProcess(models.Model):
    """
    The master tracker for a single, complete wire manufacturing process,
    from raw material to finished product. This object governs the entire flow.
    """
    # Note: A list of raw materials is linked to this process via a ForeignKey
    # in the DeviceRawMaterial model. You can access the list of raw materials
    # for a process instance with `process.raw_materials.all()`.

    # Links to the single object created at each stage of the process.
    # These are nullable because they are filled in sequentially.
    authorization = models.OneToOneField(DeviceAuthorization, on_delete=models.SET_NULL, null=True, blank=True, related_name='manufacturing_process')
    checklist = models.OneToOneField(DeviceChecklist, on_delete=models.SET_NULL, null=True, blank=True, related_name='manufacturing_process')
    production = models.OneToOneField(DeviceProduction, on_delete=models.SET_NULL, null=True, blank=True, related_name='manufacturing_process')
    product_final = models.OneToOneField('DeviceProduct', on_delete=models.SET_NULL, null=True, blank=True, related_name='manufacturing_process')

    # Current state of the master workflow
    stage = models.CharField(max_length=100, default='rawmaterial')
    current_step = models.IntegerField(default=1)
    is_completed = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(QcUserModel, on_delete=models.SET_NULL, null=True, related_name='processes_created')

    def __str__(self):
        return f"Process #{self.id} - Stage: {self.stage}, Step: {self.current_step}"


class ManufacturingProcessAction(models.Model):
    """
    Logs every action (creation, approval, rejection) taken on the master workflow.
    """
    process = models.ForeignKey(WireManufacturingProcess, on_delete=models.CASCADE, related_name='actions')
    user = models.ForeignKey(QcUserModel, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=20)
    from_stage = models.CharField(max_length=100)
    from_step = models.IntegerField()
    to_stage = models.CharField(max_length=100)
    to_step = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Action by {self.user} on Process #{self.process.id} at {self.timestamp}"


# --- DeviceProduct --------------------------------------------------
class DeviceProduct(FormSpecifications):
    form_name = models.ForeignKey(WireFormName, on_delete=models.CASCADE, related_name='device_products', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='device_products', null=True, blank=True)
    
    up_meter = models.CharField(max_length=255, blank=True, null=True)
    down_meter = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    net_weight = models.CharField(max_length=255, blank=True, null=True)
    gross_weight = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Device Product - {self.document_code}"
