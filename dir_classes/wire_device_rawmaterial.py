# apps/wire/wire_device_rawmaterial.py
from django.db import models
from .wire_abstract_class import FormSpecifications, QcTestWire, GenericRelation, WireFormName

from apps.marketing.models import Product, Customer 


# -----------------------------------------------------
class DeviceRawMaterial(FormSpecifications):
    qc_tests_wire = GenericRelation(QcTestWire)

    form_name = models.ForeignKey(WireFormName, on_delete=models.CASCADE, related_name='device_raw_materials', null=True, blank=True) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='device_raw_materials', null=True, blank=True) 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='device_raw_material_customers', null=True, blank=True)
    manufacturing_process = models.ForeignKey('wire.WireManufacturingProcess', on_delete=models.CASCADE, related_name='raw_materials', null=True, blank=True)

    def __str__(self):
        return f"Raw Material - {self.document_code}"
