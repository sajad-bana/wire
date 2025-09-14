# apps/wire/serializers.py
from rest_framework import serializers
from apps.wire.models import (
    DeviceRawMaterial, DeviceAuthorization, DeviceChecklist,
    DeviceProduction, DeviceProduct, LicenseProduction,
    RawMaterialSpecifications, Packaging, Production,
    ProductionWaste,
    QcTestWire
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



# ----------------------------------------------------------------------------
# Updated serializer classes
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
    """
    A custom field to handle the generic relationship for device settings.
    """
    def to_representation(self, value):
        if isinstance(value, FormExtruderSettings):
            return FormExtruderSettingsSerializer(value).data
        
        if isinstance(value, FormFiberWeaverSettings):
            return FormFiberWeaverSettingsSerializer(value).data
        
        if isinstance(value, FormRadiantSettings):
            return FormRadiantSettingsSerializer(value).data
        
        if isinstance(value, FormShieldWeaverSettings):
            return FormShieldWeaverSettingsSerializer(value).data
        
        raise Exception('Unexpected type of settings object')
# ----------------------------------------------------------------------------
class WireFormNameField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        if value is None:
            return None
        if hasattr(value, 'name'):
            return value.name
        else:
            try:
                full_instance = self.get_queryset().get(pk=value.pk)
                return full_instance.name
            except:
                return None


# ----------------------------------------------------------------------------
# --- Abstract Base Classes --------------------------------------------------
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


class UnsharedFieldStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnsharedFieldStructure
        fields = '__all__'


class FormSpecificationsSerializerMixin(serializers.ModelSerializer):
    """Fixed mixin with proper inheritance"""
    unshared_fields = UnsharedFieldStructureSerializer(read_only=True)
    
    unshared_fields_id = serializers.PrimaryKeyRelatedField(
        queryset=UnsharedFieldStructure.objects.all(),
        source='unshared_fields',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        abstract = True


class QcTestWireDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QcTestWireDefinition
        fields = '__all__'


class QcTestWireSerializer(serializers.ModelSerializer):
    class Meta:
        model = QcTestWire
        exclude = ['content_type', 'object_id']


class QcTestWireableModelSerializerMixin:
    """Mixin for handling nested qc_tests_wire"""
    def create(self, validated_data):
        qc_tests_wire_data = validated_data.pop('qc_tests_wire', [])
        instance = super().create(validated_data)
        for qc_test_wire_data in qc_tests_wire_data:
            QcTestWire.objects.create(content_object=instance, **qc_test_wire_data)
        return instance

    def update(self, instance, validated_data):
        qc_tests_wire_data = validated_data.pop('qc_tests_wire', None)
        instance = super().update(instance, validated_data)

        if qc_tests_wire_data is not None:
            instance.qc_tests_wire.all().delete()
            for qc_test_wire_data in qc_tests_wire_data:
                QcTestWire.objects.create(content_object=instance, **qc_test_wire_data)
        return instance


# ----------------------------------------------------------------------------
class LicenseProductionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LicenseProduction
        exclude = ['authorization']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['total_order_amount'] is None:
            representation['total_order_amount'] = {}
        if representation['aggregate_production_amount'] is None:
            representation['aggregate_production_amount'] = {}
        if representation['required_amount'] is None:
            representation['required_amount'] = {}
        return representation


# class DeviceSettingsSerializer(FormSpecificationsSerializerMixin):
#     class Meta:
#         model = DeviceSettings
#         exclude = ['authorization']


class RawMaterialSpecificationsSerializer(FormSpecificationsSerializerMixin):
    class Meta:
        model = RawMaterialSpecifications
        exclude = ['authorization']


class PackagingSerializer(FormSpecificationsSerializerMixin):
    class Meta:
        model = Packaging
        exclude = ['authorization']


class DeviceAuthorizationSerializer(FormSpecificationsSerializerMixin):
    form_name = WireFormNameField(queryset=WireFormName.objects.all(), required=False, allow_null=True)
    license_production = LicenseProductionSerializer(required=False, allow_null=True)
    
    # device_settings = DeviceSettingsSerializer(required=False, allow_null=True)
    device_settings = DeviceSettingsRelatedField(read_only=True)

    raw_material_specifications = RawMaterialSpecificationsSerializer(many=True, required=False)
    packaging = PackagingSerializer(required=False, allow_null=True)
    product = ProductSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True, required=False, allow_null=True
    )
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True, required=False, allow_null=True
    )
    
    class Meta:
        model = DeviceAuthorization
        fields = [
            'id', 'form_name', 'document_code', 'license_number', 'trace_date', 'trace_code', 'description',
            'unshared_fields', 'license_production', 'device_settings', 
            'raw_material_specifications', 'packaging', 'product', 'customer',
            'product_id', 'customer_id', 'unshared_fields_id'
        ]
    
    def create(self, validated_data):
        license_production_data = validated_data.pop('license_production', None)
        raw_material_specifications_data = validated_data.pop('raw_material_specifications', [])
        packaging_data = validated_data.pop('packaging', None)

        authorization = DeviceAuthorization.objects.create(**validated_data)
        
        if license_production_data:
            LicenseProduction.objects.create(authorization=authorization, **license_production_data)

        if packaging_data:
            Packaging.objects.create(authorization=authorization, **packaging_data)
        
        for spec_data in raw_material_specifications_data:
            RawMaterialSpecifications.objects.create(authorization=authorization, **spec_data)
            
        return authorization

    def update(self, instance, validated_data):
        license_production_data = validated_data.pop('license_production', None)
        raw_material_specifications_data = validated_data.pop('raw_material_specifications', None)
        packaging_data = validated_data.pop('packaging', None)

        # Update parent instance
        instance = super().update(instance, validated_data)

        # Handle OneToOne LicenseProduction
        if license_production_data is not None:
            license_instance = getattr(instance, 'license_production', None)
            if license_instance:
                # Update existing instance
                for attr, value in license_production_data.items():
                    setattr(license_instance, attr, value)
                license_instance.save()
            else:
                # Create new instance if it doesn't exist
                LicenseProduction.objects.create(authorization=instance, **license_production_data)

        # Handle OneToOne Packaging
        if packaging_data is not None:
            packaging_instance = getattr(instance, 'packaging', None)
            if packaging_instance:
                for attr, value in packaging_data.items():
                    setattr(packaging_instance, attr, value)
                packaging_instance.save()
            else:
                Packaging.objects.create(authorization=instance, **packaging_data)
                
        # Handle ForeignKey RawMaterialSpecifications (many=True)
        if raw_material_specifications_data is not None:
            # Simple strategy: delete existing and create new ones.
            instance.raw_material_specifications.all().delete()
            for spec_data in raw_material_specifications_data:
                RawMaterialSpecifications.objects.create(authorization=instance, **spec_data)

        return instance



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
        exclude = ['device_production']



class DeviceProductionSerializer(FormSpecificationsSerializerMixin):
    form_name = WireFormNameField(queryset=WireFormName.objects.all(), required=False, allow_null=True)
    production = ProductionSerializer(many=True, required=False)  # Just added many=True
    production_wastes = ProductionWasteSerializer(many=True, required=False)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = DeviceProduction
        fields = [
            'id', 'form_name', 'document_code', 'license_number', 'trace_date', 'trace_code', 'description',
            'unshared_fields', 'production', 'production_wastes',
            'product', 'product_id', 'unshared_fields_id'
        ]

    def create(self, validated_data):
        production_data = validated_data.pop('production', [])  # Now expects a list
        production_wastes_data = validated_data.pop('production_wastes', [])
        
        device_production = DeviceProduction.objects.create(**validated_data)
        
        # Handle multiple production entries
        for production_item in production_data:
            production_qc_test_data = production_item.pop('production_qc_test', {})
            production = Production.objects.create(device_production=device_production, **production_item)
            
            # Create appropriate QC test based on form name
            self._create_production_qc_test(device_production, production, production_qc_test_data)
        
        for waste_data in production_wastes_data:
            ProductionWaste.objects.create(device_production=device_production, **waste_data)
            
        return device_production

    def update(self, instance, validated_data):
        production_data = validated_data.pop('production', None)
        production_wastes_data = validated_data.pop('production_wastes', None)
        
        # Update parent instance
        instance = super().update(instance, validated_data)
        
        # Handle ForeignKey Production entries (many=True)
        if production_data is not None:
            # Delete existing production entries and create new ones
            instance.production.all().delete()
            for production_item in production_data:
                production_qc_test_data = production_item.pop('production_qc_test', {})
                production = Production.objects.create(device_production=instance, **production_item)
                self._create_production_qc_test(instance, production, production_qc_test_data)
        
        # Handle ForeignKey ProductionWastes (many=True)
        if production_wastes_data is not None:
            instance.production_wastes.all().delete()
            for waste_data in production_wastes_data:
                ProductionWaste.objects.create(device_production=instance, **waste_data)
        
        return instance

    def _create_production_qc_test(self, device_production, production, qc_test_data):
        """Create appropriate QC test based on form name"""
        form_name = device_production.form_name.name if device_production.form_name else None

        qc_test_instance = None
        if form_name == 'Extruder':
            qc_test_serializer = ProductionExtruderQcTestWireSerializer(data=qc_test_data)
            if qc_test_serializer.is_valid(raise_exception=True):
                qc_test_instance = qc_test_serializer.save(production=production)
        elif form_name == 'Radiant':
            qc_test_serializer = ProductionRadiantQcTestWireSerializer(data=qc_test_data)
            if qc_test_serializer.is_valid(raise_exception=True):
                qc_test_instance = qc_test_serializer.save(production=production)
        elif form_name == 'FiberWeaver':
            qc_test_serializer = ProductionFiberWeaverQcTestWireSerializer(data=qc_test_data)
            if qc_test_serializer.is_valid(raise_exception=True):
                qc_test_instance = qc_test_serializer.save(production=production)
        elif form_name == 'ShieldWeaver':
            qc_test_serializer = ProductionShieldWeaverQcTestWireSerializer(data=qc_test_data)
            if qc_test_serializer.is_valid(raise_exception=True):
                qc_test_instance = qc_test_serializer.save(production=production)

        # Link the QC test instance to the production instance
        if qc_test_instance:
            production.production_qc_test = qc_test_instance
            production.save()


class DeviceRawMaterialSerializer(QcTestWireableModelSerializerMixin, FormSpecificationsSerializerMixin):
    form_name = WireFormNameField(queryset=WireFormName.objects.all(), required=False, allow_null=True)
    qc_tests_wire = QcTestWireSerializer(many=True, required=False)
    product = ProductSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True, required=False, allow_null=True
    )
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = DeviceRawMaterial
        fields = [
            'id', 'form_name', 'document_code', 'license_number', 'trace_date', 'trace_code', 'description',
            'unshared_fields', 'product', 'customer', 'qc_tests_wire',
            'product_id', 'customer_id', 'unshared_fields_id'
        ]


class DeviceChecklistSerializer(QcTestWireableModelSerializerMixin, FormSpecificationsSerializerMixin):
    form_name = WireFormNameField(queryset=WireFormName.objects.all(), required=False, allow_null=True)
    qc_tests_wire = QcTestWireSerializer(many=True, required=False)
    product = ProductSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True, required=False, allow_null=True
    )
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True, required=False, allow_null=True
    )
    
    class Meta:
        model = DeviceChecklist
        fields = [
            'id', 'form_name', 'document_code', 'license_number', 'trace_date', 'trace_code', 'description',
            'unshared_fields', 'product', 'customer', 'qc_tests_wire',
            'product_id', 'customer_id', 'unshared_fields_id',
            'work_shift', 'amount_test_samples'
        ]


class DeviceProductSerializer(FormSpecificationsSerializerMixin):
    form_name = WireFormNameField(queryset=WireFormName.objects.all(), required=False, allow_null=True)
    product = ProductSerializer(read_only=True)
    # customer = CustomerSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True, required=False, allow_null=True
    )
    # customer_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Customer.objects.all(), source='customer', write_only=True, required=False, allow_null=True
    # )

    class Meta:
        model = DeviceProduct
        fields = [
            'id', 'form_name', 'document_code', 'license_number', # title
            'product_id', 'product', #'technical_code', # name & code & standard prooduct
            
            'up_meter', 'down_meter', # up & down meter
            'color', 'size', # color & size
            'trace_date', 'trace_code', # code & data trace
            'net_weight', 'gross_weight', # Net & Gross weight 
            'description', # option

            # 'unshared_fields', # 'customer',
            #'production',
             #'customer_id', 
            # 'unshared_fields_id'
        ]