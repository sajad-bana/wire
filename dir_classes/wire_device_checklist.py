# apps/wire/wire_device_checklist.py
from django.db import models
from .wire_abstract_class import FormSpecifications, QcTestWire, GenericRelation, WireFormName

from apps.marketing.models import Product, Customer 


# -----------------------------------------------------
class DeviceChecklist(FormSpecifications):
    qc_tests_wire = GenericRelation(QcTestWire)

    form_name = models.ForeignKey(WireFormName, on_delete=models.CASCADE, related_name='device_checklists', null=True, blank=True) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='device_checklists', null=True, blank=True) 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='device_checklist_customers', null=True, blank=True)

    WORK_SHIFT_CHOICES = [
            ('shift1', 'shift1'),
            ('shift2', 'shift2'),
            ('shift3', 'shift3')
        ]

    work_shift = models.CharField(
            max_length=20,
            choices=WORK_SHIFT_CHOICES,
            default='RawMaterials',
            null=True,
            blank=True,
        )
    
    amount_test_samples = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Checklist - {self.document_code}"