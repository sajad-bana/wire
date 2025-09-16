# apps/wire/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # Lookups (Restored)
    UnsharedFieldStructureViewSet,
    QcTestWireDefinitionViewSet,
    MaterialViewSet,
    CoatingMaterialViewSet,
    WireFormNameViewSet,
    # Forms
    DeviceRawMaterialViewSet, DeviceAuthorizationViewSet, DeviceChecklistViewSet,
    DeviceProductionViewSet, DeviceProductViewSet,
    # Master Workflow
    StartManufacturingProcessView, ManufacturingProcessDetailView, PerformProcessActionView
)

# Router for all ViewSets
router = DefaultRouter()

# Lookups Wire (Restored) - Grouped under a 'lookups' prefix for clarity
router.register(r'lookups/unshared-field-structures', UnsharedFieldStructureViewSet, basename='unsharedfieldstructure')
router.register(r'lookups/qc-test-wire-definitions', QcTestWireDefinitionViewSet, basename='qctestwiredefinition')
router.register(r'lookups/materials', MaterialViewSet, basename='material')
router.register(r'lookups/coating-materials', CoatingMaterialViewSet, basename='coatingmaterial')
router.register(r'lookups/wire-form-names', WireFormNameViewSet, basename='wireformname')

# Forms Wire - Grouped under a 'forms' prefix for clarity
router.register(r'forms/raw-materials', DeviceRawMaterialViewSet, basename='devicerawmaterial')
router.register(r'forms/authorizations', DeviceAuthorizationViewSet, basename='deviceauthorization')
router.register(r'forms/checklists', DeviceChecklistViewSet, basename='devicechecklist')
router.register(r'forms/productions', DeviceProductionViewSet, basename='deviceproduction')
router.register(r'forms/products', DeviceProductViewSet, basename='deviceproduct')

# Explicit paths for the master workflow management
urlpatterns = [
    # Include all endpoints from the router
    path('', include(router.urls)),
    
    # Master Workflow URLs
    path('workflow/process/start/', StartManufacturingProcessView.as_view(), name='manufacturing-process-start'),
    path('workflow/process/<int:pk>/', ManufacturingProcessDetailView.as_view(), name='manufacturing-process-detail'),
    path('workflow/process/<int:pk>/action/', PerformProcessActionView.as_view(), name='manufacturing-process-action'),
]

