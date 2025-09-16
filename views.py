# apps/wire/views.py
from rest_framework import viewsets, mixins, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError


# Correctly and explicitly import all necessary models from their specific files
from .models import (
    DeviceRawMaterial, DeviceAuthorization, DeviceChecklist, DeviceProduction, DeviceProduct,
    WireManufacturingProcess
)
# Import lookup models from their specific location
from .dir_classes.wire_abstract_class import (
    UnsharedFieldStructure, QcTestWireDefinition, Material, CoatingMaterial, WireFormName
)

from .serializers import (
    UnsharedFieldStructureSerializer, QcTestWireDefinitionSerializer,
    MaterialSerializer, CoatingMaterialSerializer, WireFormNameSerializer,
    DeviceRawMaterialSerializer, DeviceAuthorizationSerializer, DeviceChecklistSerializer,
    DeviceProductionSerializer, DeviceProductSerializer, WireManufacturingProcessSerializer,
    FormExtruderSettingsSerializer, FormFiberWeaverSettingsSerializer, FormRadiantSettingsSerializer, FormShieldWeaverSettingsSerializer
)
from .pagination import CustomPagination
from .services import ManufacturingWorkflowService
from .permissions import IsSuperUser, CanCreateFormForStage, CanUpdateFormForStage

# --- Lookups ViewSets (Restored) ---

@extend_schema(tags=['Wire - Lookups'])
class UnsharedFieldStructureViewSet(viewsets.ModelViewSet):
    queryset = UnsharedFieldStructure.objects.order_by('pk').all()
    serializer_class = UnsharedFieldStructureSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

@extend_schema(tags=['Wire - Lookups'])
class QcTestWireDefinitionViewSet(viewsets.ModelViewSet):
    queryset = QcTestWireDefinition.objects.order_by('pk').all()
    serializer_class = QcTestWireDefinitionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

@extend_schema(tags=['Wire - Lookups'])
class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.order_by('pk').all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

@extend_schema(tags=['Wire - Lookups'])
class CoatingMaterialViewSet(viewsets.ModelViewSet):
    queryset = CoatingMaterial.objects.order_by('pk').all()
    serializer_class = CoatingMaterialSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

@extend_schema(tags=['Wire - Lookups'])
class WireFormNameViewSet(viewsets.ModelViewSet):
    queryset = WireFormName.objects.order_by('pk').all()
    serializer_class = WireFormNameSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


# --- Form ViewSets with Workflow Permissions ---

class BaseWorkflowViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet for forms that are part of the master workflow.
    It links form creation/updates to the master process.
    """
    pagination_class = CustomPagination
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [CanCreateFormForStage]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [CanUpdateFormForStage]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    # The conflicting create method has been removed. 
    # The default behavior from ModelViewSet will now be used, 
    # which correctly calls the custom create method in the serializer.


@extend_schema(tags=['Wire - Forms'])
class DeviceRawMaterialViewSet(BaseWorkflowViewSet):
    queryset = DeviceRawMaterial.objects.all()
    serializer_class = DeviceRawMaterialSerializer
    pagination_class = CustomPagination

@extend_schema(tags=['Wire - Forms'])
class DeviceAuthorizationViewSet(BaseWorkflowViewSet):
    queryset = DeviceAuthorization.objects.all()
    serializer_class = DeviceAuthorizationSerializer
    pagination_class = CustomPagination

    @extend_schema(
        examples=[
            OpenApiExample(
                'Extruder Form Example',
                summary='Creating DeviceAuthorization with Extruder settings',
                description='Example for form_name="Extruder" with specific device settings.',
                value={
                    "workflow_id": 1,
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
                    "workflow_id": 1,
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
                    "workflow_id": 1,
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
                    "workflow_id": 1,
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
                    "workflow_id": 1,
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
class DeviceChecklistViewSet(BaseWorkflowViewSet):
    queryset = DeviceChecklist.objects.all()
    serializer_class = DeviceChecklistSerializer
    pagination_class = CustomPagination

@extend_schema(tags=['Wire - Forms'])
class DeviceProductionViewSet(BaseWorkflowViewSet):
    queryset = DeviceProduction.objects.all()
    serializer_class = DeviceProductionSerializer
    pagination_class = CustomPagination

@extend_schema(tags=['Wire - Forms'])
class DeviceProductViewSet(BaseWorkflowViewSet):
    queryset = DeviceProduct.objects.all()
    serializer_class = DeviceProductSerializer
    pagination_class = CustomPagination


# --- Master Workflow API Views (Refactored to simple APIViews) ---

@extend_schema(tags=['Wire - Master Workflow'])
class StartManufacturingProcessView(APIView):
    """Starts a new master manufacturing process."""
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Start a new master manufacturing process", request=None, responses={201: WireManufacturingProcessSerializer})
    def post(self, request, *args, **kwargs):
        service = ManufacturingWorkflowService(user=request.user)
        process = service.start_process()
        serializer = WireManufacturingProcessSerializer(process)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(tags=['Wire - Master Workflow'])
class ManufacturingProcessDetailView(APIView):
    """Retrieve or delete a master manufacturing process."""
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsSuperUser()]
        return super().get_permissions()

    @extend_schema(summary="Get the status of a specific manufacturing process", responses={200: WireManufacturingProcessSerializer})
    def get(self, request, pk, *args, **kwargs):
        try:
            process = WireManufacturingProcess.objects.get(pk=pk)
            serializer = WireManufacturingProcessSerializer(process)
            return Response(serializer.data)
        except WireManufacturingProcess.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(summary="Delete a master process (Superuser only)")
    def delete(self, request, pk, *args, **kwargs):
        service = ManufacturingWorkflowService(user=request.user)
        try:
            service.delete_process(process_id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)


class PerformActionPayloadSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    comment = serializers.CharField(required=False, allow_blank=True)

@extend_schema(tags=['Wire - Master Workflow'])
class PerformProcessActionView(APIView):
    """Approve or reject a step in the master workflow."""
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Approve or reject a step in the master workflow", request=PerformActionPayloadSerializer, responses={200: WireManufacturingProcessSerializer})
    def post(self, request, pk, *args, **kwargs):
        serializer = PerformActionPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service = ManufacturingWorkflowService(user=request.user)
        try:
            updated_process = service.approve_or_reject_step(
                process_id=pk,
                **serializer.validated_data
            )
            response_serializer = WireManufacturingProcessSerializer(updated_process)
            return Response(response_serializer.data)
        except (ValidationError, PermissionDenied) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except WireManufacturingProcess.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

