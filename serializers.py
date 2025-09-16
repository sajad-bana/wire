# apps/wire/serializers.py
from rest_framework import serializers
from apps.wire.models import (
    DeviceRawMaterial, DeviceAuthorization, DeviceChecklist,
    DeviceProduction, DeviceProduct, LicenseProduction,
    RawMaterialSpecifications, Packaging, Production,
    ProductionWaste,
    QcTestWire,
    WireManufacturingProcess, ManufacturingProcessAction
)
from .dir_classes.wire_abstract_class import (
    QcTestWireDefinition,
    Material, CoatingMaterial, WireFormName,
    UnsharedFieldStructure
)
from .dir_classes.device_settings import(
    FormExtruderSettings, FormFiberWeaverSettings, FormRadiantSettings, FormShieldWeaverSettings
)
from .dir_classes.production_qc_settings import (
    ProductionExtruderQcTestWire, ProductionRadiantQcTestWire,
    ProductionFiberWeaverQcTestWire, ProductionShieldWeaverQcTestWire
)
from apps.marketing.serializers import ProductSerializer, CustomerSerializer
from apps.marketing.models import Product, Customer

# --- Base Serializers for Workflow Forms ---

class BaseWorkflowFormSerializer(serializers.ModelSerializer):
    """
    Base serializer that includes the 'workflow_id' field, which is required
    for creation but is not part of the models themselves.
    """
    workflow_id = serializers.IntegerField(write_only=True, required=True, help_text="The ID of the master manufacturing process.")

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        # Make workflow_id not required for updates (PATCH/PUT)
        if self.instance is not None:
            fields['workflow_id'].required = False
        return fields

    def create(self, validated_data):
        # Pop the 'workflow_id' to prevent it from being passed to the model constructor,
        # where it would cause a TypeError.
        workflow_id = validated_data.pop('workflow_id')

        # Create the form instance (e.g., DeviceAuthorization) with the remaining clean data.
        instance = super().create(validated_data)

        # Now, link the newly created instance to its master workflow process.
        model_name = self.Meta.model._meta.model_name.lower()
        
        try:
            process = WireManufacturingProcess.objects.get(pk=workflow_id)

            # Handle the one-to-many relationship for DeviceRawMaterial
            if isinstance(instance, DeviceRawMaterial):
                instance.manufacturing_process = process
                instance.save()
            
            # Handle one-to-one relationships for all other models
            else:
                model_field_map = {
                    'deviceauthorization': 'authorization',
                    'devicechecklist': 'checklist',
                    'deviceproduction': 'production',
                    'deviceproduct': 'product_final',
                }
                model_field_name = model_field_map.get(model_name)
                
                if model_field_name and hasattr(process, model_field_name):
                    setattr(process, model_field_name, instance)
                    process.save()

            # Refresh the instance from the database to reflect the new relationship.
            instance.refresh_from_db()
        except WireManufacturingProcess.DoesNotExist:
            raise serializers.ValidationError(f"Workflow with id {workflow_id} not found.")
        
        return instance

# ----------------------------------------------------------------------------
# --- Nested Serializers for DeviceAuthorization ---
class FormExtruderSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormExtruderSettings
        exclude = ('authorization',)

class FormRadiantSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormRadiantSettings
        exclude = ('authorization',)

class FormFiberWeaverSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormFiberWeaverSettings
        exclude = ('authorization',)

class FormShieldWeaverSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormShieldWeaverSettings
        exclude = ('authorization',)

class DeviceSettingsRelatedField(serializers.RelatedField):
    """A custom field to handle the generic relationship for device settings."""
    def to_representation(self, value):
        if isinstance(value, FormExtruderSettings): return FormExtruderSettingsSerializer(value).data
        if isinstance(value, FormFiberWeaverSettings): return FormFiberWeaverSettingsSerializer(value).data
        if isinstance(value, FormRadiantSettings): return FormRadiantSettingsSerializer(value).data
        if isinstance(value, FormShieldWeaverSettings): return FormShieldWeaverSettingsSerializer(value).data
        raise Exception('Unexpected type of settings object')

# --- Lookups & Helper Serializers ---

class WireFormNameField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return value.name if value else None

class UnsharedFieldStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnsharedFieldStructure
        fields = '__all__'
        
class QcTestWireDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QcTestWireDefinition
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class CoatingMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoatingMaterial
        fields = '__all__'

class WireFormNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = WireFormName
        fields = '__all__'


class QcTestWireSerializer(serializers.ModelSerializer):
    class Meta:
        model = QcTestWire
        exclude = ['content_type', 'object_id']


class QcTestWireableModelSerializerMixin:
    """Mixin for handling nested qc_tests_wire for creation and updates."""
    def _handle_qc_tests(self, instance, qc_tests_data):
        if qc_tests_data is None:
            return
            
        if self.instance is None:
             for test_data in qc_tests_data:
                QcTestWire.objects.create(content_object=instance, **test_data)
             return

        existing_test_ids = {test.id for test in instance.qc_tests_wire.all()}
        incoming_test_ids = {test.get('id') for test in qc_tests_data if test.get('id')}

        for test_data in qc_tests_data:
            test_id = test_data.pop('id', None)
            if test_id in existing_test_ids:
                test_instance = QcTestWire.objects.get(id=test_id, object_id=instance.id)
                for attr, value in test_data.items():
                    setattr(test_instance, attr, value)
                test_instance.save()
            else:
                QcTestWire.objects.create(content_object=instance, **test_data)
        
        for test_id in existing_test_ids - incoming_test_ids:
            QcTestWire.objects.filter(id=test_id, object_id=instance.id).delete()

    def update(self, instance, validated_data):
        qc_tests_data = validated_data.pop('qc_tests_wire', None)
        instance = super().update(instance, validated_data)
        self._handle_qc_tests(instance, qc_tests_data)
        return instance

# --- Nested Form Serializers ---
class LicenseProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseProduction
        exclude = ['id', 'authorization']

class RawMaterialSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialSpecifications
        exclude = ['id', 'authorization']

class PackagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packaging
        exclude = ['id', 'authorization']

# --------------------
class ProductionExtruderQcTestWireSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionExtruderQcTestWire
        exclude = ('production',)

class ProductionRadiantQcTestWireSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionRadiantQcTestWire
        exclude = ('production',)

class ProductionFiberWeaverQcTestWireSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionFiberWeaverQcTestWire
        exclude = ('production',)

class ProductionShieldWeaverQcTestWireSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionShieldWeaverQcTestWire
        exclude = ('production',)

class ProductionQcTestWireRelatedField(serializers.RelatedField):
    """
    A custom field to handle the generic relationship for production QC tests.
    """
    def to_representation(self, value):
        if isinstance(value, ProductionExtruderQcTestWire):
            return ProductionExtruderQcTestWireSerializer(value).data
        
        if isinstance(value, ProductionRadiantQcTestWire):
            return ProductionRadiantQcTestWireSerializer(value).data
        
        if isinstance(value, ProductionFiberWeaverQcTestWire):
            return ProductionFiberWeaverQcTestWireSerializer(value).data
        
        if isinstance(value, ProductionShieldWeaverQcTestWire):
            return ProductionShieldWeaverQcTestWireSerializer(value).data
        
        raise Exception('Unexpected type of QC test object')

class ProductionSerializer(serializers.ModelSerializer):
    production_qc_test = ProductionQcTestWireRelatedField(read_only=True)
    
    class Meta:
        model = Production
        exclude = ['device_production', 'qc_test_content_type', 'qc_test_object_id']


# --------------------

class ProductionWasteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionWaste
        exclude = ['id', 'device_production']

# --- Main Form Serializers ---

class DeviceAuthorizationSerializer(BaseWorkflowFormSerializer):
    license_production = LicenseProductionSerializer(required=False, allow_null=True)
    device_settings = DeviceSettingsRelatedField(read_only=True)
    raw_material_specifications = RawMaterialSpecificationsSerializer(many=True, required=False)
    packaging = PackagingSerializer(required=False, allow_null=True)
    stage = serializers.ReadOnlyField(source='manufacturing_process.stage', read_only=True)
    current_step = serializers.ReadOnlyField(source='manufacturing_process.current_step', read_only=True)
    
    class Meta:
        model = DeviceAuthorization
        fields = '__all__' 

    def create(self, validated_data):
        license_data = validated_data.pop('license_production', None)
        specs_data = validated_data.pop('raw_material_specifications', [])
        packaging_data = validated_data.pop('packaging', None)
        
        # This now calls the fixed create method in the base class
        instance = super().create(validated_data)
        
        if license_data: LicenseProduction.objects.create(authorization=instance, **license_data)
        if packaging_data: Packaging.objects.create(authorization=instance, **packaging_data)
        for spec in specs_data: RawMaterialSpecifications.objects.create(authorization=instance, **spec)
        
        return instance

class DeviceRawMaterialSerializer(QcTestWireableModelSerializerMixin, BaseWorkflowFormSerializer):
    qc_tests_wire = QcTestWireSerializer(many=True, required=False)
    stage = serializers.ReadOnlyField(source='manufacturing_process.stage', read_only=True)
    current_step = serializers.ReadOnlyField(source='manufacturing_process.current_step', read_only=True)
    
    class Meta:
        model = DeviceRawMaterial
        fields = '__all__'
        extra_kwargs = {
            # The manufacturing_process is set programmatically, so it's not required in the input.
            'manufacturing_process': {'required': False, 'allow_null': True}
        }

    def create(self, validated_data):
        qc_tests_data = validated_data.pop('qc_tests_wire', [])
        # The base serializer now handles workflow linking, so we just call super()
        instance = super().create(validated_data)
        self._handle_qc_tests(instance, qc_tests_data)
        return instance

class DeviceChecklistSerializer(QcTestWireableModelSerializerMixin, BaseWorkflowFormSerializer):
    qc_tests_wire = QcTestWireSerializer(many=True, required=False)
    stage = serializers.ReadOnlyField(source='manufacturing_process.stage', read_only=True)
    current_step = serializers.ReadOnlyField(source='manufacturing_process.current_step', read_only=True)

    class Meta:
        model = DeviceChecklist
        fields = '__all__'
    
    def create(self, validated_data):
        qc_tests_data = validated_data.pop('qc_tests_wire', [])
        instance = super().create(validated_data)
        self._handle_qc_tests(instance, qc_tests_data)
        return instance

    def update(self, instance, validated_data):
        qc_tests_data = validated_data.pop('qc_tests_wire', None)
        instance = super().update(instance, validated_data)
        if qc_tests_data is not None:
            self._handle_qc_tests(instance, qc_tests_data)
        return instance

class DeviceProductionSerializer(BaseWorkflowFormSerializer):
    production = ProductionSerializer(many=True, required=False)
    production_wastes = ProductionWasteSerializer(many=True, required=False)
    stage = serializers.ReadOnlyField(source='manufacturing_process.stage', read_only=True)
    current_step = serializers.ReadOnlyField(source='manufacturing_process.current_step', read_only=True)
    
    class Meta:
        model = DeviceProduction
        fields = '__all__'

    def create(self, validated_data):
        production_data = validated_data.pop('production', [])
        wastes_data = validated_data.pop('production_wastes', [])
        
        # Call the parent create method to handle workflow linking
        instance = super().create(validated_data)
        
        # Now create the nested objects
        for prod_item in production_data:
            Production.objects.create(device_production=instance, **prod_item)
            
        for waste_item in wastes_data:
            ProductionWaste.objects.create(device_production=instance, **waste_item)
            
        return instance

    def update(self, instance, validated_data):
        production_data = validated_data.pop('production', None)
        wastes_data = validated_data.pop('production_wastes', None)
        
        instance = super().update(instance, validated_data)
        
        if production_data is not None:
            # This simple update logic assumes you might want to replace existing
            # production records. A more complex logic might be needed to update
            # existing records based on an ID.
            instance.production.all().delete()
            for prod_item in production_data:
                Production.objects.create(device_production=instance, **prod_item)
                    
        if wastes_data is not None:
            instance.production_wastes.all().delete()
            for waste_item in wastes_data:
                ProductionWaste.objects.create(device_production=instance, **waste_item)
                
        return instance

class DeviceProductSerializer(BaseWorkflowFormSerializer):
    stage = serializers.ReadOnlyField(source='manufacturing_process.stage', read_only=True)
    current_step = serializers.ReadOnlyField(source='manufacturing_process.current_step', read_only=True)
    
    class Meta:
        model = DeviceProduct
        fields = '__all__'

# --- Master Workflow Serializers ---

class ManufacturingProcessActionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = ManufacturingProcessAction
        fields = '__all__'

class WireManufacturingProcessSerializer(serializers.ModelSerializer):
    raw_materials = DeviceRawMaterialSerializer(many=True, read_only=True) # Changed from raw_material
    authorization = DeviceAuthorizationSerializer(read_only=True)
    checklist = DeviceChecklistSerializer(read_only=True)
    production = DeviceProductionSerializer(read_only=True)
    product_final = DeviceProductSerializer(read_only=True)
    actions = ManufacturingProcessActionSerializer(many=True, read_only=True)
    
    class Meta:
        model = WireManufacturingProcess
        fields = '__all__'
