from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ShipmentViewSet, DeliveryPersonViewSet, test_post

router = DefaultRouter()
# 1) Register delivery-persons first
router.register(r'delivery-persons', DeliveryPersonViewSet, basename='delivery-person')
# 2) Then shipments at the root
router.register(r'', ShipmentViewSet, basename='shipment')

urlpatterns = router.urls + [
    path('test-post/', test_post, name='test-post'),
]
