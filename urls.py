# apps/wire/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DeviceRawMaterialViewSet, DeviceAuthorizationViewSet, DeviceChecklistViewSet,
    DeviceProductionViewSet,DeviceProductViewSet,
    QcTestWireDefinitionViewSet,
    UnsharedFieldStructureViewSet,
    MaterialViewSet, CoatingMaterialViewSet, WireFormNameViewSet,
)

# -----------------------------------------------------
router = DefaultRouter()

# Lookups Wire
router.register(r'unshared-field-structures', UnsharedFieldStructureViewSet, basename='unsharedfieldstructure')
router.register(r'qc-test-wire-definitions', QcTestWireDefinitionViewSet, basename='qctestwiredefinition')
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'coating-materials', CoatingMaterialViewSet, basename='coatingmaterial')
router.register(r'wire-form-names', WireFormNameViewSet, basename='wireformname')

# Forms Wire
router.register(r'raw-materials', DeviceRawMaterialViewSet, basename='devicerawmaterial')
router.register(r'authorizations', DeviceAuthorizationViewSet, basename='deviceauthorization')
router.register(r'checklists', DeviceChecklistViewSet, basename='devicechecklist')
router.register(r'productions', DeviceProductionViewSet, basename='deviceproduction')
router.register(r'products', DeviceProductViewSet, basename='deviceproduct')

urlpatterns = [
    path('', include(router.urls)),
]