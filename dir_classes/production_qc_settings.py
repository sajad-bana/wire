# wire/dir_classes/production_qc_settings.py
from django.db import models


# --- BaseProductionQcTestWire --------------------------------------------------
class BaseProductionQcTestWire(models.Model):
    production = models.ForeignKey(
        'wire.Production',
        on_delete=models.CASCADE,
        related_name='%(class)s_qc_tests'
    )
    operator_approval = models.BooleanField(default=False, blank=True, null=True)
    quality_control_approval = models.BooleanField(default=False, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


# -----------------------------------------------------------------------------
class ProductionExtruderQcTestWire(BaseProductionQcTestWire):
    # All boolean fields for Extruder QC tests
    sample_approval = models.BooleanField(default=False, blank=True, null=True)
    wire_diameter = models.BooleanField(default=False, blank=True, null=True)
    noise_diameter_fluctuation = models.BooleanField(default=False, blank=True, null=True)
    spark = models.BooleanField(default=False, blank=True, null=True)
    bump = models.BooleanField(default=False, blank=True, null=True)
    surface_smoothness = models.BooleanField(default=False, blank=True, null=True)
    connection_test = models.BooleanField(default=False, blank=True, null=True)
    die_size = models.BooleanField(default=False, blank=True, null=True)
    nozzle_size = models.BooleanField(default=False, blank=True, null=True)
    temperature = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"Extruder QC Test for {self.production}"


class ProductionRadiantQcTestWire(BaseProductionQcTestWire):
    # All boolean fields for Radiant QC tests
    pretwist_connection_test = models.BooleanField(default=False, blank=True, null=True)
    cable_strand_count_control = models.BooleanField(default=False, blank=True, null=True)
    cable_appearance_control = models.BooleanField(default=False, blank=True, null=True)
    teflon_tape_not_broken = models.BooleanField(default=False, blank=True, null=True)
    cable_layout_control = models.BooleanField(default=False, blank=True, null=True)
    product_connection_test = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"Radiant QC Test for {self.production}"


class ProductionFiberWeaverQcTestWire(BaseProductionQcTestWire):
    # Mixed field types for FiberWeaver QC tests
    tissue_density_control = models.CharField(max_length=255, blank=True, null=True)  # String type
    no_tearing_fraying = models.BooleanField(default=False, blank=True, null=True)
    no_tissue_dirt = models.BooleanField(default=False, blank=True, null=True)
    gear_control = models.BooleanField(default=False, blank=True, null=True)
    machine_speed = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"FiberWeaver QC Test for {self.production}"


class ProductionShieldWeaverQcTestWire(BaseProductionQcTestWire):
    # All string fields for ShieldWeaver QC tests
    appearance = models.CharField(max_length=255, blank=True, null=True)
    weave_density = models.CharField(max_length=255, blank=True, null=True)
    number_wire_strands = models.CharField(max_length=255, blank=True, null=True)
    connection_test = models.CharField(max_length=255, blank=True, null=True)
    final_length = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"ShieldWeaver QC Test for {self.production}"