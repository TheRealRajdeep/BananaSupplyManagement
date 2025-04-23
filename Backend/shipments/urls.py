# shipments/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import ShipmentViewSet

router = routers.DefaultRouter()
router.register(r'shipments', ShipmentViewSet, basename='shipment')

urlpatterns = [
    path('', include(router.urls)),
]