# apps/wire/models.py

from .dir_classes.wire_device_rawmaterial import *
from .dir_classes.wire_license_production import *
from .dir_classes.wire_device_checklist import *
from .dir_classes.wire_device_production import *

from .dir_classes.production_qc_settings import *

from apps.marketing.models import Product


# --- DeviceProduct --------------------------------------------------
class DeviceProduct(FormSpecifications):
    form_name = models.ForeignKey(WireFormName, on_delete=models.CASCADE, related_name='device_products', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='device_products', null=True, blank=True)
    production = models.ForeignKey(DeviceProduction, on_delete=models.SET_NULL, null=True, related_name='device_products')
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='device_product_customers', null=True, blank=True)

    up_meter = models.CharField(max_length=255, blank=True, null=True)
    down_meter = models.CharField(max_length=255, blank=True, null=True)

    color = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)

    net_weight = models.CharField(max_length=255, blank=True, null=True)
    gross_weight = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Device Product - {self.document_code}"