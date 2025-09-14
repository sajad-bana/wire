# apps/wire/wire_abstract_class.py
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


# -----------------------------------------------------
# --- Abstract Base Classes ---
# -----------------------------------------------------
class FormSpecifications(models.Model):

    document_code = models.CharField(max_length=255)
    license_number = models.CharField(max_length=255, blank=True, null=True)

    trace_date = models.DateField(unique=False)
    trace_code = models.CharField(max_length=255, unique=True)

    description = models.TextField(blank=True, null=True)
    
    # Change from JSONField to ForeignKey
    unshared_fields = models.ForeignKey(
        'wire.UnsharedFieldStructure', 
        on_delete=models.SET_NULL, 
        related_name='%(class)s_unshared_fields',
        null=True, 
        blank=True
    )

    class Meta:
        abstract = True


# -----------------------------------------------------
class QcTestWireDefinition(models.Model):
    TYPE_FORM_CHOICES = [
            ('Authorizations', 'authorizations'),
            ('RawMaterials', 'rawmaterials'),
            ('Checklists', 'checklists'),
            ('Productions', 'productions'),
            ('Products', 'products')
        ]

    type_form = models.CharField(
            max_length=20,
            choices=TYPE_FORM_CHOICES,
            default='RawMaterials',
            null=True,
            blank=True,
        )
    
    test_table = models.CharField(max_length=255, blank=True, null=True)

    test_type = models.CharField(max_length=255, blank=True, null=True)
    test_description = models.TextField(blank=True, null=True)
    control_tool = models.CharField(max_length=255, blank=True, null=True)
    standard_technical_criterion = models.FileField(upload_to='standards/', blank=True, null=True)

    def __str__(self):
        return self.test_type or f"QcTestWire Definition {self.id}"


class QcTestWire(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Test data fields
    test_definition = models.ForeignKey(
        QcTestWireDefinition,
        on_delete=models.SET_NULL,
        related_name='qc_tests_wire',
        null=True,
        blank=True
    )
    test_result = models.BooleanField(default=True, blank=True, null=True)
    operator_approval = models.BooleanField(default=True, blank=True, null=True)
    quality_control_approval = models.BooleanField(default=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)


# -----------------------------------------------------
class Material(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    def __str__(self):
        return self.name


class CoatingMaterial(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    def __str__(self):
        return self.name



# -----------------------------------------------------
# class WireFormName(models.Model):

#     TYPE_FORM_CHOICES = [
#             ('Authorizations', 'authorizations'),
#             ('RawMaterials', 'rawmaterials'),
#             ('Checklists', 'checklists'),
#             ('Productions', 'productions'),
#             ('Products', 'products')
#         ]

#     type_form = models.CharField(
#             max_length=20,
#             choices=TYPE_FORM_CHOICES,
#             default='RawMaterials',
#             null=True,
#             blank=True,
#         )

#     name = models.CharField(max_length=255, unique=True, null=True, blank=True)
#     # type_form = models.CharField(max_length=255, unique=True, null=True, blank=True)
#     def __str__(self):
#         return(f"{self.name} \t {self.type_form}")
class WireFormName(models.Model):

    TYPE_FORM_CHOICES = [
            ('Authorizations', 'authorizations'),
            ('RawMaterials', 'rawmaterials'),
            ('Checklists', 'checklists'),
            ('Productions', 'productions'),
            ('Products', 'products')
        ]

    type_form = models.CharField(
            max_length=20,
            choices=TYPE_FORM_CHOICES,
            default='RawMaterials',
            null=True,
            blank=True,
        )

    # Remove unique=True from here
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'type_form'], name='unique_name_and_type_form')
        ]

    def __str__(self):
        return(f"{self.name} \t {self.type_form}")


# -----------------------------------------------------
class UnsharedFieldStructure(models.Model):
    """
    A model to store predefined structures for the 'unshared_fields' JSON field.
    """
    name = models.CharField(max_length=255, unique=True, help_text="A unique name for the structure, used for searching.")
    structure = models.JSONField(help_text="The JSON structure template.")

    def __str__(self):
        return self.name
