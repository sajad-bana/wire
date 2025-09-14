# apps/wire/views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import *
from .dir_classes.wire_abstract_class import *
from .dir_classes.device_settings import *
from .dir_classes.production_qc_settings import (
    ProductionExtruderQcTestWire, ProductionRadiantQcTestWire,
    ProductionFiberWeaverQcTestWire, ProductionShieldWeaverQcTestWire
)

from .serializers import (
    DeviceRawMaterialSerializer, DeviceAuthorizationSerializer, DeviceChecklistSerializer,
    DeviceProductionSerializer, 
    DeviceProductSerializer,
    QcTestWireDefinitionSerializer, UnsharedFieldStructureSerializer,
    MaterialSerializer, CoatingMaterialSerializer, WireFormNameSerializer,
    FormExtruderSettingsSerializer, FormFiberWeaverSettingsSerializer, FormRadiantSettingsSerializer, FormShieldWeaverSettingsSerializer
)
from .permissions import IsAdminOrReadOnly, IsManagerOrAdmin, IsOperator
from .pagination import CustomPagination


# Lookups-----------------------------------------------------
@extend_schema(tags=['Wire - Lookups'])
class UnsharedFieldStructureViewSet(viewsets.ModelViewSet):
    queryset = UnsharedFieldStructure.objects.order_by('pk').all()
    serializer_class = UnsharedFieldStructureSerializer
    permission_classes = [IsManagerOrAdmin]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


@extend_schema(tags=['Wire - Lookups'])
class QcTestWireDefinitionViewSet(viewsets.ModelViewSet):
    queryset = QcTestWireDefinition.objects.order_by('pk').all()
    serializer_class = QcTestWireDefinitionSerializer
    permission_classes = [IsManagerOrAdmin]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter] 
    search_fields = ['test_table']


@extend_schema(tags=['Wire - Lookups'])
class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.order_by('pk').all()
    serializer_class = MaterialSerializer
    permission_classes = [IsManagerOrAdmin]
    pagination_class = CustomPagination


@extend_schema(tags=['Wire - Lookups'])
class CoatingMaterialViewSet(viewsets.ModelViewSet):
    queryset = CoatingMaterial.objects.order_by('pk').all()
    serializer_class = CoatingMaterialSerializer
    permission_classes = [IsManagerOrAdmin]
    pagination_class = CustomPagination


@extend_schema(tags=['Wire - Lookups'])
class WireFormNameViewSet(viewsets.ModelViewSet):
    queryset = WireFormName.objects.order_by('pk').all()
    serializer_class = WireFormNameSerializer
    permission_classes = [IsManagerOrAdmin]
    pagination_class = CustomPagination


# Forms-----------------------------------------------------
@extend_schema(tags=['Wire - Forms'])
class DeviceRawMaterialViewSet(viewsets.ModelViewSet):
    queryset = DeviceRawMaterial.objects.select_related(
        'form_name', 'product', 'customer', 'unshared_fields'
    ).prefetch_related('qc_tests_wire').order_by('pk').all()
    serializer_class = DeviceRawMaterialSerializer
    permission_classes = [IsManagerOrAdmin]
    pagination_class = CustomPagination


@extend_schema(tags=['Wire - Forms'])
class DeviceAuthorizationViewSet(viewsets.ModelViewSet):
    queryset = DeviceAuthorization.objects.select_related(
        'form_name', 'product', 'customer', 'unshared_fields',
        'license_production', 'packaging'
    ).prefetch_related(
        'device_settings',
        'raw_material_specifications',
        'raw_material_specifications__unshared_fields'
    ).order_by('pk').all()
    serializer_class = DeviceAuthorizationSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination

    @extend_schema(
        examples=[
            OpenApiExample(
                'Extruder Form Example',
                summary='Creating DeviceAuthorization with Extruder settings',
                description='Example for form_name="Extruder" with specific device settings.',
                value={
                    "form_name": 1,
                    "document_code": "AUTH-2025-001",
                    "license_number": "LIC-EXT-123",
                    "trace_date": "2025-09-15",
                    "trace_code": "TRACE-EXT-456",
                    "description": "Authorization for extruder production",
                    "product_id": 1,
                    "customer_id": 1,
                    "device_settings": {
                        "insulation_thickness": 2.5,
                        "wire_outer_diameter": 3.2,
                        "mold_size": 2.8,
                        "nozzle_size": 2.0,
                        "preheater_temperature": 180.0,
                        "dryer_temperature": 200.0,
                        "hot_water_bath_temperature": 60.0,
                        "screw_speed": 45.0,
                        "linear_speed": 15.5,
                        "tensile_force": 120.0,
                        "vacuum_pressure": 0.8,
                        "spark_regulation_voltage_tester": 220.0,
                        "lamp_accuracy": 0.1,
                        "host_temp_zone_1": 195.0,
                        "host_temp_zone_2": 210.0,
                        "host_temp_zone_3": 225.0,
                        "host_temp_zone_4": 240.0,
                        "host_neck_temp": 245.0,
                        "host_head_temp": 250.0,
                        "host_dies_temp": 255.0,
                        "accumulator_traction": "Medium",
                        "speed_take_up": "Normal",
                        "traverse_range_take_up": "Full",
                        "corona_treatment": "Enabled",
                        "insulation_type": "PVC",
                        "insulation_color": "Blue",
                        "ring_type": "single_line",
                        "line_color": "Red",
                        "color_percentage": "100%",
                        "extruder_die_size_line_female": "2.5mm",
                        "extruder_nozzle_size_female": "2.0mm",
                        "medron_speed": "Standard",
                        "injecter_temp_zone_1": "200",
                        "injecter_temp_zone_2": "205",
                        "injecter_temp_zone_3": "210",
                        "print_type": "Inkjet",
                        "print_direction": "Forward",
                        "size": "Medium",
                        "font": "Arial",
                        "color": "Black",
                        "print_speed": "Fast",
                        "text": "Sample Text",
                        "output_spool_size": "Large",
                        "initial_sample_size": "10m",
                        "percentage_conductor_waste": "5%",
                        "percentage_insulation_waste": "3%",
                        "percentage_pigment_waste": "2%",
                        "subsequent_sampling_length": "50m"
                    }
                }
            ),
            OpenApiExample(
                'Radiant Form Example',
                summary='Creating DeviceAuthorization with Radiant settings',
                description='Example for form_name="Radiant" with specific device settings.',
                value={
                    "form_name": 2,
                    "document_code": "AUTH-2025-002",
                    "license_number": "LIC-RAD-123",
                    "trace_date": "2025-09-15",
                    "trace_code": "TRACE-RAD-456",
                    "description": "Authorization for radiant production",
                    "product_id": 1,
                    "customer_id": 1,
                    "device_settings": {
                        "number_input_threads": "24",
                        "required_production_meterage": "1000m",
                        "wrap_length": "25.0",
                        "wrap_length_tolerance": "±0.5",
                        "wrap_direction": "Left",
                        "taper_position": "Center",
                        "strip_type": "Copper",
                        "strip_width": "12.5",
                        "strip_width_tolerance": "±0.1",
                        "strip_thickness": "0.5",
                        "strip_thickness_tolerance": "±0.05",
                        "strip_color": "Natural",
                        "strip_direction": "Clockwise",
                        "tensile_force": "120N",
                        "overlap_percentage": "10%",
                        "output_spool_size": "Large",
                        "initial_sample_size": "10m",
                        "percentage_conductor_waste": "4%",
                        "percentage_insulation_waste": "2%",
                        "percentage_pigment_waste": "1%",
                        "subsequent_sampling_length": "100m"
                    }
                }
            ),
            OpenApiExample(
                'ShieldWeaver Form Example',
                summary='Creating DeviceAuthorization with ShieldWeaver settings',
                description='Example for form_name="ShieldWeaver" with specific device settings.',
                value={
                    "form_name": 3,
                    "document_code": "AUTH-2025-003",
                    "license_number": "LIC-SW-123",
                    "trace_date": "2025-09-15",
                    "trace_code": "TRACE-SW-456",
                    "description": "Authorization for shield weaver production",
                    "product_id": 1,
                    "customer_id": 1,
                    "device_settings": {
                        "number_spindles": "16",
                        "weave_density_percentage": "85.5%",
                        "fiber_type": "Glass",
                        "fiber_color": "White",
                        "machine_speed": "120 rpm",
                        "tensile_force": "95N",
                        "outer_width_product": "15.2mm",
                        "inner_diameter_product": "8.5mm",
                        "tissue_density_percentage": "90%",
                        "z1": "Zone 1 Setting",
                        "z2": "Zone 2 Setting",
                        "z3": "Zone 3 Setting",
                        "z4": "Zone 4 Setting",
                        "output_spool_size": "Medium",
                        "initial_sample_size": "15m",
                        "percentage_conductor_waste": "6%",
                        "percentage_insulation_waste": "3%",
                        "percentage_pigment_waste": "2%",
                        "subsequent_sampling_length": "75m"
                    }
                }
            ),
            OpenApiExample(
                'FiberWeaver Form Example',
                summary='Creating DeviceAuthorization with FiberWeaver settings',
                description='Example for form_name="FiberWeaver" with specific device settings.',
                value={
                    "form_name": 4,
                    "document_code": "AUTH-2025-004",
                    "license_number": "LIC-FW-123",
                    "trace_date": "2025-09-15",
                    "trace_code": "TRACE-FW-456",
                    "description": "Authorization for fiber weaver production",
                    "product_id": 1,
                    "customer_id": 1,
                    "device_settings": {
                        "number_input_coils": "8",
                        "number_upper_coils": "4",
                        "number_lower_coils": "4",
                        "wire_type": "Steel",
                        "number_wires_per_coil": "12",
                        "diameter_each_wire": "0.5mm",
                        "machine_speed": "95 rpm",
                        "z1": "Zone 1 Config",
                        "z2": "Zone 2 Config", 
                        "z3": "Zone 3 Config",
                        "z4": "Zone 4 Config",
                        "tensile_force": "110N",
                        "product_outer_width": "14.8mm",
                        "product_inner_diameter": "7.2mm",
                        "strip_condition": "Excellent",
                        "strip_width": "10.5",
                        "strip_width_tolerance": "±0.2",
                        "strip_thickness": "0.3",
                        "strip_thickness_tolerance": "±0.03",
                        "strip_color": "Silver",
                        "overlap_percentage": "15%",
                        "tissue_density_percentage": "88%",
                        "output_spool_size": "Large",
                        "initial_sample_size": "12m",
                        "percentage_conductor_waste": "5%",
                        "percentage_insulation_waste": "4%",
                        "percentage_pigment_waste": "3%",
                        "subsequent_sampling_length": "80m"
                    }
                }
            ),
            OpenApiExample(
                'Complete Authorization Example',
                summary='Full DeviceAuthorization with all nested data',
                description='Complete example including packaging and raw material specifications.',
                value={
                    "form_name": 1,
                    "document_code": "AUTH-2025-005",
                    "license_number": "LIC-FULL-123",
                    "trace_date": "2025-09-15",
                    "trace_code": "TRACE-FULL-456",
                    "description": "Complete authorization example with all nested data",
                    "product_id": 1,
                    "customer_id": 1,
                    "unshared_fields_id": 1,
                    "device_settings": {
                        "insulation_thickness": 2.5,
                        "preheater_temperature": 180.0,
                        "linear_speed": 15.5,
                        "lamp_accuracy": 0.1,
                        "accumulator_tension": 50.0,
                        "wire_outer_diameter": 3.2,
                        "dryer_temperature": 200.0,
                        "tensile_force": 120.0,
                        "die_size": 2.8,
                        "vacuum_pressure": 0.8
                    },
                    "license_production": {
                        "setup_license_number": "SETUP-FULL-789",
                        "order_number": "PO-2025-104",
                        "technical_attachment_code": "TECH-005",
                        "cms_code": "CMS-005",
                        "product_description": "Complete production with all specifications",
                        "total_order_amount": [
                            {"length": 2000, "strand": 4, "type": "Type A"},
                            {"length": 3000, "strand": 8, "type": "Type B"}
                        ],
                        "aggregate_production_amount": [
                            {"length": 2050, "strand": 4, "type": "Type A"},
                            {"length": 3050, "strand": 8, "type": "Type B"}
                        ],
                        "required_amount": [
                            {"length": 1980, "strand": 4, "type": "Type A"},
                            {"length": 2980, "strand": 8, "type": "Type B"}
                        ]
                    },
                    "packaging": {
                        "packaging_type": "Steel Reel",
                        "packaging_quantity": "10 units",
                        "packaging_size": "Large",
                        "final_packaging": "Wooden crates",
                        "instruction": "Handle with care",
                        "description": "Premium packaging for industrial cables",
                        "unshared_fields_id": 1
                    },
                    "raw_material_specifications": [
                        {
                            "raw_material_type": "Aluminum",
                            "raw_material_amount": "800kg",
                            "required_amount_including_waste": "850kg",
                            "product_code": "AL-99.7",
                            "trace_code": "TRACE-AL-001",
                            "description": "High purity aluminum wire",
                            "unshared_fields_id": 1
                        },
                        {
                            "raw_material_type": "Copper",
                            "raw_material_amount": "500kg",
                            "required_amount_including_waste": "520kg",
                            "product_code": "CU-99.9",
                            "trace_code": "TRACE-CU-001",
                            "description": "Ultra pure copper strands",
                            "unshared_fields_id": 1
                        }
                    ]
                }
            )
        ]
    )

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # First, save the DeviceAuthorization instance
        authorization = serializer.save()

        # Then, create the appropriate settings instance based on the form_name
        form_name = authorization.form_name.name if authorization.form_name else None
        settings_data = self.request.data.get('device_settings', {})

        settings_instance = None
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

        # Link the settings instance to the authorization instance
        if settings_instance:
            authorization.device_settings = settings_instance
            authorization.save()


@extend_schema(tags=['Wire - Forms'])
class DeviceChecklistViewSet(viewsets.ModelViewSet):
    queryset = DeviceChecklist.objects.select_related(
        'form_name', 'product', 'customer', 'unshared_fields'
    ).prefetch_related('qc_tests_wire').order_by('pk').all()
    serializer_class = DeviceChecklistSerializer
    permission_classes = [IsManagerOrAdmin]  # Fixed permission logic
    pagination_class = CustomPagination


@extend_schema(tags=['Wire - Forms'])
class DeviceProductionViewSet(viewsets.ModelViewSet):
    queryset = DeviceProduction.objects.select_related(
        'form_name', 'product'
    ).prefetch_related(
        'production_wastes',
        'productions',  # Changed from 'production__production_qc_tests_wire' to 'productions'
        'productions__production_qc_test'  # Added to prefetch QC tests
    ).order_by('pk').all()
    serializer_class = DeviceProductionSerializer
    permission_classes = [IsManagerOrAdmin]
    pagination_class = CustomPagination

    @extend_schema(
        examples=[
            OpenApiExample(
                'Extruder Production Example',
                summary='Creating DeviceProduction with Extruder QC tests',
                description='Example for form_name="Extruder" with production as an array.',
                value={
                    "form_name": 1,
                    "document_code": "PROD-2025-001",
                    "license_number": "LIC-EXT-PROD-123",
                    "trace_date": "2025-09-15",
                    "trace_code": "TRACE-EXT-PROD-456",
                    "description": "Production authorization for extruder cable manufacturing",
                    "product_id": 1,
                    "unshared_fields_id": 1,
                    "production": [
                        {
                            "operator_name": "John Smith",
                            "start_date": "2025-09-15",
                            "end_date": "2025-09-16",
                            "input_spool_length": "5000m",
                            "input_spool_number": "SP-EXT-001",
                            "output_spool_length": "4850m",
                            "output_spool_number": "SP-EXT-OUT-001",
                            "input_tank_number": "TANK-EXT-01",
                            "output_tank_number": "TANK-EXT-02",
                            "input_spool_remaining_length": "150m",
                            "operator_approval": True,
                            "quality_control_approval": True,
                            "description": "First shift extruder production run",
                            "production_qc_test": {
                                "sample_approval": True,
                                "wire_diameter": True,
                                "noise_diameter_fluctuation": False,
                                "spark": True,
                                "bump": True,
                                "surface_smoothness": True,
                                "connection_test": True,
                                "die_size": True,
                                "nozzle_size": True,
                                "temperature": True,
                                "operator_approval": True,
                                "quality_control_approval": True,
                                "description": "All extruder QC tests passed for first shift"
                            }
                        },
                        {
                            "operator_name": "Jane Doe",
                            "start_date": "2025-09-16",
                            "end_date": "2025-09-17",
                            "input_spool_length": "4500m",
                            "input_spool_number": "SP-EXT-002",
                            "output_spool_length": "4350m",
                            "output_spool_number": "SP-EXT-OUT-002",
                            "input_tank_number": "TANK-EXT-02",
                            "output_tank_number": "TANK-EXT-03",
                            "input_spool_remaining_length": "150m",
                            "operator_approval": True,
                            "quality_control_approval": True,
                            "description": "Second shift extruder production run",
                            "production_qc_test": {
                                "sample_approval": True,
                                "wire_diameter": True,
                                "noise_diameter_fluctuation": True,
                                "spark": True,
                                "bump": False,
                                "surface_smoothness": True,
                                "connection_test": True,
                                "die_size": True,
                                "nozzle_size": True,
                                "temperature": True,
                                "operator_approval": True,
                                "quality_control_approval": True,
                                "description": "Second shift QC tests passed"
                            }
                        }
                    ],
                    "production_wastes": [
                        {
                            "waste_type": "Copper Scrap",
                            "waste_amount": "5.2kg"
                        },
                        {
                            "waste_type": "Insulation Waste",
                            "waste_amount": "2.8kg"
                        },
                        {
                            "waste_type": "PVC Pellets Waste",
                            "waste_amount": "1.5kg"
                        }
                    ]
                }
            ),
            OpenApiExample(
                'Radiant Production Example',
                summary='Creating DeviceProduction with Radiant QC tests',
                description='Example for form_name="Radiant" with production as an array.',
                value={
                    "form_name": 2,
                    "document_code": "PROD-2025-002",
                    "license_number": "LIC-RAD-PROD-123",
                    "trace_date": "2025-09-15",
                    "trace_code": "TRACE-RAD-PROD-456",
                    "description": "Production authorization for radiant cable manufacturing",
                    "product_id": 2,
                    "unshared_fields_id": 2,
                    "production": [
                        {
                            "operator_name": "Sarah Wilson",
                            "start_date": "2025-09-15",
                            "end_date": "2025-09-16",
                            "input_spool_length": "3000m",
                            "input_spool_number": "SP-RAD-001",
                            "output_spool_length": "2900m",
                            "output_spool_number": "SP-RAD-OUT-001",
                            "input_tank_number": "TANK-RAD-01",
                            "output_tank_number": "TANK-RAD-02",
                            "input_spool_remaining_length": "100m",
                            "operator_approval": True,
                            "quality_control_approval": True,
                            "description": "Morning shift radiant production",
                            "production_qc_test": {
                                "pretwist_connection_test": True,
                                "cable_strand_count_control": True,
                                "cable_appearance_control": True,
                                "teflon_tape_not_broken": True,
                                "cable_layout_control": True,
                                "product_connection_test": True,
                                "operator_approval": True,
                                "quality_control_approval": True,
                                "description": "All radiant QC tests passed for morning shift"
                            }
                        },
                        {
                            "operator_name": "Tom Brown",
                            "start_date": "2025-09-16",
                            "end_date": "2025-09-17",
                            "input_spool_length": "2800m",
                            "input_spool_number": "SP-RAD-002",
                            "output_spool_length": "2700m",
                            "output_spool_number": "SP-RAD-OUT-002",
                            "input_tank_number": "TANK-RAD-02",
                            "output_tank_number": "TANK-RAD-03",
                            "input_spool_remaining_length": "100m",
                            "operator_approval": True,
                            "quality_control_approval": False,
                            "description": "Evening shift radiant production - needs review",
                            "production_qc_test": {
                                "pretwist_connection_test": True,
                                "cable_strand_count_control": False,
                                "cable_appearance_control": True,
                                "teflon_tape_not_broken": True,
                                "cable_layout_control": True,
                                "product_connection_test": True,
                                "operator_approval": True,
                                "quality_control_approval": False,
                                "description": "Cable strand count control failed - needs recheck"
                            }
                        },
                        {
                            "operator_name": "Mike Johnson",
                            "start_date": "2025-09-17",
                            "end_date": "2025-09-18",
                            "input_spool_length": "3200m",
                            "input_spool_number": "SP-RAD-003",
                            "output_spool_length": "3100m",
                            "output_spool_number": "SP-RAD-OUT-003",
                            "input_tank_number": "TANK-RAD-03",
                            "output_tank_number": "TANK-RAD-04",
                            "input_spool_remaining_length": "100m",
                            "operator_approval": True,
                            "quality_control_approval": True,
                            "description": "Night shift radiant production",
                            "production_qc_test": {
                                "pretwist_connection_test": True,
                                "cable_strand_count_control": True,
                                "cable_appearance_control": True,
                                "teflon_tape_not_broken": True,
                                "cable_layout_control": True,
                                "product_connection_test": True,
                                "operator_approval": True,
                                "quality_control_approval": True,
                                "description": "Perfect night shift - all tests passed"
                            }
                        }
                    ],
                    "production_wastes": [
                        {
                            "waste_type": "Strip Material Waste",
                            "waste_amount": "3.1kg"
                        },
                        {
                            "waste_type": "Teflon Tape Waste",
                            "waste_amount": "0.8kg"
                        }
                    ]
                }
            ),
            OpenApiExample(
                'FiberWeaver Production Example',
                summary='Creating DeviceProduction with FiberWeaver QC tests',
                description='Example for form_name="FiberWeaver" with production as an array.',
                value={
                    "form_name": 3,
                    "document_code": "PROD-2025-003",
                    "license_number": "LIC-FW-PROD-123",
                    "trace_date": "2025-09-15",
                    "trace_code": "TRACE-FW-PROD-456",
                    "description": "Production authorization for fiber weaver manufacturing",
                    "product_id": 3,
                    "unshared_fields_id": 3,
                    "production": [
                        {
                            "operator_name": "Alice Cooper",
                            "start_date": "2025-09-15",
                            "end_date": "2025-09-16",
                            "input_spool_length": "4000m",
                            "input_spool_number": "SP-FW-001",
                            "output_spool_length": "3850m",
                            "output_spool_number": "SP-FW-OUT-001",
                            "input_tank_number": "TANK-FW-01",
                            "output_tank_number": "TANK-FW-02",
                            "input_spool_remaining_length": "150m",
                            "operator_approval": True,
                            "quality_control_approval": True,
                            "description": "First shift fiber weaver production",
                            "production_qc_test": {
                                "tissue_density_control": "85% density maintained throughout production",
                                "no_tearing_fraying": True,
                                "no_tissue_dirt": True,
                                "gear_control": True,
                                "machine_speed": True,
                                "operator_approval": True,
                                "quality_control_approval": True,
                                "description": "All fiber weaver QC tests passed for first shift"
                            }
                        },
                        {
                            "operator_name": "Bob Martinez",
                            "start_date": "2025-09-16",
                            "end_date": "2025-09-17",
                            "input_spool_length": "3500m",
                            "input_spool_number": "SP-FW-002",
                            "output_spool_length": "3400m",
                            "output_spool_number": "SP-FW-OUT-002",
                            "input_tank_number": "TANK-FW-02",
                            "output_tank_number": "TANK-FW-03",
                            "input_spool_remaining_length": "100m",
                            "operator_approval": True,
                            "quality_control_approval": False,
                            "description": "Second shift fiber weaver production - quality issues",
                            "production_qc_test": {
                                "tissue_density_control": "75% density - below specification",
                                "no_tearing_fraying": False,
                                "no_tissue_dirt": True,
                                "gear_control": True,
                                "machine_speed": False,
                                "operator_approval": True,
                                "quality_control_approval": False,
                                "description": "Density and tearing issues detected - needs rework"
                            }
                        }
                    ],
                    "production_wastes": [
                        {
                            "waste_type": "Fiber Material Waste",
                            "waste_amount": "2.7kg"
                        },
                        {
                            "waste_type": "Defective Tissue Waste",
                            "waste_amount": "1.9kg"
                        }
                    ]
                }
            ),
            OpenApiExample(
                'ShieldWeaver Production Example',
                summary='Creating DeviceProduction with ShieldWeaver QC tests',
                description='Example for form_name="ShieldWeaver" with production as an array.',
                value={
                    "form_name": 4,
                    "document_code": "PROD-2025-004",
                    "license_number": "LIC-SW-PROD-123",
                    "trace_date": "2025-09-15",
                    "trace_code": "TRACE-SW-PROD-456",
                    "description": "Production authorization for shield weaver manufacturing",
                    "product_id": 4,
                    "unshared_fields_id": 4,
                    "production": [
                        {
                            "operator_name": "Carol Davis",
                            "start_date": "2025-09-15",
                            "end_date": "2025-09-16",
                            "input_spool_length": "3500m",
                            "input_spool_number": "SP-SW-001",
                            "output_spool_length": "3400m",
                            "output_spool_number": "SP-SW-OUT-001",
                            "input_tank_number": "TANK-SW-01",
                            "output_tank_number": "TANK-SW-02",
                            "input_spool_remaining_length": "100m",
                            "operator_approval": True,
                            "quality_control_approval": True,
                            "description": "First shift shield weaver production",
                            "production_qc_test": {
                                "appearance": "Excellent - no visible defects, uniform weave pattern",
                                "weave_density": "90% - within specifications (88-92%)",
                                "number_wire_strands": "24 strands counted and verified",
                                "connection_test": "All connections secure and tested at 150% load",
                                "final_length": "3400m measured and verified",
                                "operator_approval": True,
                                "quality_control_approval": True,
                                "description": "Perfect first shift - all shield weaver QC tests passed"
                            }
                        },
                        {
                            "operator_name": "David Wilson",
                            "start_date": "2025-09-16",
                            "end_date": "2025-09-17",
                            "input_spool_length": "3200m",
                            "input_spool_number": "SP-SW-002",
                            "output_spool_length": "3100m",
                            "output_spool_number": "SP-SW-OUT-002",
                            "input_tank_number": "TANK-SW-02",
                            "output_tank_number": "TANK-SW-03",
                            "input_spool_remaining_length": "100m",
                            "operator_approval": True,
                            "quality_control_approval": True,
                            "description": "Second shift shield weaver production",
                            "production_qc_test": {
                                "appearance": "Good - minor surface variations within tolerance",
                                "weave_density": "89% - acceptable within range",
                                "number_wire_strands": "24 strands confirmed",
                                "connection_test": "All connections passed standard tests",
                                "final_length": "3100m verified",
                                "operator_approval": True,
                                "quality_control_approval": True,
                                "description": "Good second shift production"
                            }
                        },
                        {
                            "operator_name": "Eva Rodriguez",
                            "start_date": "2025-09-17",
                            "end_date": "2025-09-18",
                            "input_spool_length": "2800m",
                            "input_spool_number": "SP-SW-003",
                            "output_spool_length": "2650m",
                            "output_spool_number": "SP-SW-OUT-003",
                            "input_tank_number": "TANK-SW-03",
                            "output_tank_number": "TANK-SW-04",
                            "input_spool_remaining_length": "150m",
                            "operator_approval": False,
                            "quality_control_approval": False,
                            "description": "Third shift shield weaver production - issues detected",
                            "production_qc_test": {
                                "appearance": "Poor - visible gaps and uneven weave density",
                                "weave_density": "78% - below minimum specification of 85%",
                                "number_wire_strands": "22 strands - 2 strands missing",
                                "connection_test": "Connection failed at 120% load test",
                                "final_length": "2650m - significant waste detected",
                                "operator_approval": False,
                                "quality_control_approval": False,
                                "description": "Multiple failures - production rejected, needs investigation"
                            }
                        }
                    ],
                    "production_wastes": [
                        {
                            "waste_type": "Wire Strand Waste",
                            "waste_amount": "4.5kg"
                        },
                        {
                            "waste_type": "Shield Material Waste",
                            "waste_amount": "3.2kg"
                        },
                        {
                            "waste_type": "Defective Weave Waste",
                            "waste_amount": "2.8kg"
                        }
                    ]
                }
            ),
            OpenApiExample(
                'Complete Mixed Production Example',
                summary='Comprehensive production example with all possible fields',
                description='Complete example showing all available fields and nested relationships for Extruder form.',
                value={
                    "form_name": 1,
                    "document_code": "PROD-2025-COMPLETE-001",
                    "license_number": "LIC-COMPLETE-PROD-456",
                    "trace_date": "2025-09-15",
                    "trace_code": "TRACE-COMPLETE-789",
                    "description": "Complete comprehensive production authorization example with all fields",
                    "product_id": 1,
                    "customer_id": 1,
                    "unshared_fields_id": 1,
                    "production": [
                        {
                            "operator_name": "Senior Operator John Smith",
                            "start_date": "2025-09-15",
                            "end_date": "2025-09-16",
                            "input_spool_length": "10000m",
                            "input_spool_number": "SP-COMPLETE-INPUT-001",
                            "output_spool_length": "9750m",
                            "output_spool_number": "SP-COMPLETE-OUTPUT-001",
                            "input_tank_number": "TANK-COMPLETE-IN-A1",
                            "output_tank_number": "TANK-COMPLETE-OUT-B1",
                            "input_spool_remaining_length": "250m",
                            "operator_approval": True,
                            "quality_control_approval": True,
                            "description": "Comprehensive high-volume production run with full quality checks and monitoring",
                            "production_qc_test": {
                                "sample_approval": True,
                                "wire_diameter": True,
                                "noise_diameter_fluctuation": False,
                                "spark": True,
                                "bump": True,
                                "surface_smoothness": True,
                                "connection_test": True,
                                "die_size": True,
                                "nozzle_size": True,
                                "temperature": True,
                                "operator_approval": True,
                                "quality_control_approval": True,
                                "description": "Comprehensive QC testing completed - all parameters within specification limits, excellent production quality achieved"
                            }
                        }
                    ],
                    "production_wastes": [
                        {
                            "waste_type": "Premium Copper Scrap",
                            "waste_amount": "15.7kg"
                        },
                        {
                            "waste_type": "High-Grade Insulation Waste",
                            "waste_amount": "8.3kg"
                        },
                        {
                            "waste_type": "PVC Pellets Waste",
                            "waste_amount": "4.2kg"
                        },
                        {
                            "waste_type": "Packaging Material Waste",
                            "waste_amount": "2.1kg"
                        }
                    ]
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


@extend_schema(tags=['Wire - Forms'])
class DeviceProductViewSet(viewsets.ModelViewSet):
    queryset = DeviceProduct.objects.select_related(
        'form_name', 'product',# 'customer', 'unshared_fields', 'production'
    ).order_by('pk').all()
    serializer_class = DeviceProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination