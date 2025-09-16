# wire/dir_classes/wire_license_production.py
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db import models  # Fixed import
from .wire_abstract_class import FormSpecifications, WireFormName
from apps.marketing.models import Product, Customer 


# -----------------------------------------------------
class DeviceAuthorization(FormSpecifications):
    form_name = models.ForeignKey(WireFormName, on_delete=models.CASCADE, related_name='device_authorizations', null=True, blank=True) 
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='device_authorizations', null=True, blank=True) 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='device_authorization_customers', null=True, blank=True)

    # Generic Foreign Key to the settings models
    settings_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    settings_object_id = models.PositiveIntegerField(null=True, blank=True)
    device_settings = GenericForeignKey('settings_content_type', 'settings_object_id')



# -----------------------------------------------------
class LicenseProduction(models.Model):
    authorization = models.OneToOneField(DeviceAuthorization, on_delete=models.CASCADE, related_name='license_production')

    setup_license_number = models.CharField(max_length=255)
    order_number = models.CharField(max_length=255, blank=True, null=True)

    total_order_amount = models.JSONField(help_text="[length=1, strand=1]", blank=True, null=True)
    aggregate_production_amount = models.JSONField(help_text="[length=1, strand=1]", blank=True, null=True)
    required_amount = models.JSONField(help_text="[length=1, strand=1]", blank=True, null=True)
    
    technical_attachment_code = models.CharField(max_length=255, blank=True, null=True)
    cms_code = models.CharField(max_length=255, blank=True, null=True)
    product_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"License {self.setup_license_number}"


class RawMaterialSpecifications(models.Model):
    authorization = models.ForeignKey(DeviceAuthorization, on_delete=models.CASCADE, related_name='raw_material_specifications')

    raw_material_amount = models.CharField(max_length=255, blank=True, null=True)
    raw_material_type = models.CharField(max_length=255, blank=True, null=True)
    required_amount_including_waste = models.CharField(max_length=255, blank=True, null=True)
    product_code = models.CharField(max_length=255, blank=True, null=True)
    trace_code = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    unshared_fields = models.ForeignKey(
        'wire.UnsharedFieldStructure', 
        on_delete=models.SET_NULL, 
        related_name='raw_material_specifications',
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"Raw Material Spec - {self.raw_material_type}"


class Packaging(models.Model):
    authorization = models.OneToOneField(DeviceAuthorization, on_delete=models.CASCADE, related_name='packaging')

    packaging_type = models.CharField(max_length=255, blank=True, null=True)
    packaging_quantity = models.CharField(max_length=255, blank=True, null=True)
    packaging_size = models.CharField(max_length=255, blank=True, null=True)
    final_packaging = models.CharField(max_length=255, blank=True, null=True)
    instruction = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    unshared_fields = models.ForeignKey(
        'wire.UnsharedFieldStructure', 
        on_delete=models.SET_NULL, 
        related_name='packaging',
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"Packaging - {self.packaging_type}"