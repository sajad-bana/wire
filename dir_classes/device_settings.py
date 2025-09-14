# wire/dir_classes/device_settings.py
from django.db import models


# --- BaseDeviceSettings --------------------------------------------------
class BaseDeviceSettings(models.Model):
    authorization = models.OneToOneField(
        'wire.DeviceAuthorization',
        on_delete=models.CASCADE,
        related_name='%(class)s_settings'
    )

    class Meta:
        abstract = True


# -----------------------------------------------------------------------------
class FormExtruderSettings(BaseDeviceSettings):
    # Float/Decimal fields (thread type)
    insulation_thickness = models.FloatField(null=True, blank=True)
    wire_outer_diameter = models.FloatField(null=True, blank=True)
    mold_size = models.FloatField(null=True, blank=True)
    nozzle_size = models.FloatField(null=True, blank=True)
    preheater_temperature = models.FloatField(null=True, blank=True)
    dryer_temperature = models.FloatField(null=True, blank=True)
    hot_water_bath_temperature = models.FloatField(null=True, blank=True)
    screw_speed = models.FloatField(null=True, blank=True)
    linear_speed = models.FloatField(null=True, blank=True)
    tensile_force = models.FloatField(null=True, blank=True)
    vacuum_pressure = models.FloatField(null=True, blank=True)
    spark_regulation_voltage_tester = models.FloatField(null=True, blank=True)
    lamp_accuracy = models.FloatField(null=True, blank=True)
    host_temp_zone_1 = models.FloatField(null=True, blank=True)
    host_temp_zone_2 = models.FloatField(null=True, blank=True)
    host_temp_zone_3 = models.FloatField(null=True, blank=True)
    host_temp_zone_4 = models.FloatField(null=True, blank=True)
    host_neck_temp = models.FloatField(null=True, blank=True)
    host_head_temp = models.FloatField(null=True, blank=True)
    host_dies_temp = models.FloatField(null=True, blank=True)
    
    # String fields
    accumulator_traction = models.CharField(max_length=255, blank=True, null=True)
    speed_take_up = models.CharField(max_length=255, blank=True, null=True)
    traverse_range_take_up = models.CharField(max_length=255, blank=True, null=True)
    corona_treatment = models.CharField(max_length=255, blank=True, null=True)
    insulation_type = models.CharField(max_length=255, blank=True, null=True)
    insulation_color = models.CharField(max_length=255, blank=True, null=True)
    line_color = models.CharField(max_length=255, blank=True, null=True)
    color_percentage = models.CharField(max_length=255, blank=True, null=True)
    extruder_die_size_line_female = models.CharField(max_length=255, blank=True, null=True)
    extruder_nozzle_size_female = models.CharField(max_length=255, blank=True, null=True)
    medron_speed = models.CharField(max_length=255, blank=True, null=True)
    injecter_temp_zone_1 = models.CharField(max_length=255, blank=True, null=True)
    injecter_temp_zone_2 = models.CharField(max_length=255, blank=True, null=True)
    injecter_temp_zone_3 = models.CharField(max_length=255, blank=True, null=True)
    print_type = models.CharField(max_length=255, blank=True, null=True)
    print_direction = models.CharField(max_length=255, blank=True, null=True)
    size = models.CharField(max_length=255, blank=True, null=True)
    font = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    print_speed = models.CharField(max_length=255, blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    output_spool_size = models.CharField(max_length=255, blank=True, null=True)
    initial_sample_size = models.CharField(max_length=255, blank=True, null=True)
    percentage_conductor_waste = models.CharField(max_length=255, blank=True, null=True)
    percentage_insulation_waste = models.CharField(max_length=255, blank=True, null=True)
    percentage_pigment_waste = models.CharField(max_length=255, blank=True, null=True)
    subsequent_sampling_length = models.CharField(max_length=255, blank=True, null=True)
    
    # Choice field
    RING_TYPE_CHOICES = [
        ('single_line', 'Single Line'),
        ('double_line', 'Double Line'),
        ('ring', 'Ring'),
    ]
    ring_type = models.CharField(max_length=50, choices=RING_TYPE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"Extruder Settings - {self.authorization.document_code}"


class FormRadiantSettings(BaseDeviceSettings):
    # All string fields for Radiant
    number_input_threads = models.CharField(max_length=255, blank=True, null=True)
    required_production_meterage = models.CharField(max_length=255, blank=True, null=True)
    wrap_length = models.CharField(max_length=255, blank=True, null=True)
    wrap_length_tolerance = models.CharField(max_length=255, blank=True, null=True)
    wrap_direction = models.CharField(max_length=255, blank=True, null=True)
    taper_position = models.CharField(max_length=255, blank=True, null=True)
    strip_type = models.CharField(max_length=255, blank=True, null=True)
    strip_width = models.CharField(max_length=255, blank=True, null=True)
    strip_width_tolerance = models.CharField(max_length=255, blank=True, null=True)
    strip_thickness = models.CharField(max_length=255, blank=True, null=True)
    strip_thickness_tolerance = models.CharField(max_length=255, blank=True, null=True)
    strip_color = models.CharField(max_length=255, blank=True, null=True)
    strip_direction = models.CharField(max_length=255, blank=True, null=True)
    tensile_force = models.CharField(max_length=255, blank=True, null=True)
    overlap_percentage = models.CharField(max_length=255, blank=True, null=True)
    output_spool_size = models.CharField(max_length=255, blank=True, null=True)
    initial_sample_size = models.CharField(max_length=255, blank=True, null=True)
    percentage_conductor_waste = models.CharField(max_length=255, blank=True, null=True)
    percentage_insulation_waste = models.CharField(max_length=255, blank=True, null=True)
    percentage_pigment_waste = models.CharField(max_length=255, blank=True, null=True)
    subsequent_sampling_length = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Radiant Settings - {self.authorization.document_code}"


class FormShieldWeaverSettings(BaseDeviceSettings):
    # All string fields for ShieldWeaver
    number_spindles = models.CharField(max_length=255, blank=True, null=True)
    weave_density_percentage = models.CharField(max_length=255, blank=True, null=True)
    fiber_type = models.CharField(max_length=255, blank=True, null=True)
    fiber_color = models.CharField(max_length=255, blank=True, null=True)
    machine_speed = models.CharField(max_length=255, blank=True, null=True)
    tensile_force = models.CharField(max_length=255, blank=True, null=True)
    outer_width_product = models.CharField(max_length=255, blank=True, null=True)
    inner_diameter_product = models.CharField(max_length=255, blank=True, null=True)
    tissue_density_percentage = models.CharField(max_length=255, blank=True, null=True)
    z1 = models.CharField(max_length=255, blank=True, null=True)
    z2 = models.CharField(max_length=255, blank=True, null=True)
    z3 = models.CharField(max_length=255, blank=True, null=True)
    z4 = models.CharField(max_length=255, blank=True, null=True)
    output_spool_size = models.CharField(max_length=255, blank=True, null=True)
    initial_sample_size = models.CharField(max_length=255, blank=True, null=True)
    percentage_conductor_waste = models.CharField(max_length=255, blank=True, null=True)
    percentage_insulation_waste = models.CharField(max_length=255, blank=True, null=True)
    percentage_pigment_waste = models.CharField(max_length=255, blank=True, null=True)
    subsequent_sampling_length = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"ShieldWeaver Settings - {self.authorization.document_code}"


class FormFiberWeaverSettings(BaseDeviceSettings):
    # All string fields for FiberWeaver
    number_input_coils = models.CharField(max_length=255, blank=True, null=True)
    number_upper_coils = models.CharField(max_length=255, blank=True, null=True)
    number_lower_coils = models.CharField(max_length=255, blank=True, null=True)
    wire_type = models.CharField(max_length=255, blank=True, null=True)
    number_wires_per_coil = models.CharField(max_length=255, blank=True, null=True)
    diameter_each_wire = models.CharField(max_length=255, blank=True, null=True)
    machine_speed = models.CharField(max_length=255, blank=True, null=True)
    z1 = models.CharField(max_length=255, blank=True, null=True)
    z2 = models.CharField(max_length=255, blank=True, null=True)
    z3 = models.CharField(max_length=255, blank=True, null=True)
    z4 = models.CharField(max_length=255, blank=True, null=True)
    tensile_force = models.CharField(max_length=255, blank=True, null=True)
    product_outer_width = models.CharField(max_length=255, blank=True, null=True)
    product_inner_diameter = models.CharField(max_length=255, blank=True, null=True)
    strip_condition = models.CharField(max_length=255, blank=True, null=True)
    strip_width = models.CharField(max_length=255, blank=True, null=True)
    strip_width_tolerance = models.CharField(max_length=255, blank=True, null=True)
    strip_thickness = models.CharField(max_length=255, blank=True, null=True)
    strip_thickness_tolerance = models.CharField(max_length=255, blank=True, null=True)
    strip_color = models.CharField(max_length=255, blank=True, null=True)
    overlap_percentage = models.CharField(max_length=255, blank=True, null=True)
    tissue_density_percentage = models.CharField(max_length=255, blank=True, null=True)
    output_spool_size = models.CharField(max_length=255, blank=True, null=True)
    initial_sample_size = models.CharField(max_length=255, blank=True, null=True)
    percentage_conductor_waste = models.CharField(max_length=255, blank=True, null=True)
    percentage_insulation_waste = models.CharField(max_length=255, blank=True, null=True)
    percentage_pigment_waste = models.CharField(max_length=255, blank=True, null=True)
    subsequent_sampling_length = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"FiberWeaver Settings - {self.authorization.document_code}"