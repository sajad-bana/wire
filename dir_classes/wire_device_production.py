# apps/wire/wire_device_production.py
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .wire_abstract_class import FormSpecifications, WireFormName

from apps.marketing.models import Product, Customer


# -----------------------------------------------------
class DeviceProduction(FormSpecifications):
    form_name = models.ForeignKey(WireFormName, on_delete=models.CASCADE, related_name='device_productions', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='device_productions', null=True, blank=True) 

    def __str__(self):
        return f"Production - {self.document_code}"


# -----------------------------------------------------
class Production(models.Model):
    device_production = models.ForeignKey(DeviceProduction, on_delete=models.CASCADE, related_name='production')  # Changed from OneToOneField to ForeignKey
    operator_name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    # Production fields
    input_spool_length = models.CharField(max_length=255, blank=True, null=True)
    input_spool_number = models.CharField(max_length=255, blank=True, null=True)
    output_spool_length = models.CharField(max_length=255, blank=True, null=True)
    output_spool_number = models.CharField(max_length=255, blank=True, null=True)
    input_tank_number = models.CharField(max_length=255, blank=True, null=True)
    output_tank_number = models.CharField(max_length=255, blank=True, null=True)
    input_spool_remaining_length = models.CharField(max_length=255, blank=True, null=True)
    operator_approval = models.BooleanField(default=False, blank=True, null=True)
    quality_control_approval = models.BooleanField(default=False, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Generic Foreign Key to the QC test models
    qc_test_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    qc_test_object_id = models.PositiveIntegerField(null=True, blank=True)
    production_qc_test = GenericForeignKey('qc_test_content_type', 'qc_test_object_id')

    def __str__(self):
        return f"Production {self.operator_name} - {self.input_spool_number or 'N/A'}"


class ProductionWaste(models.Model):
    device_production = models.ForeignKey(DeviceProduction, on_delete=models.CASCADE, related_name='production_wastes')
    waste_type = models.CharField(max_length=255, blank=True, null=True)
    waste_amount = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Waste {self.waste_type} - {self.waste_amount}"