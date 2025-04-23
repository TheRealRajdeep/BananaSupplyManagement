import tempfile
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    action, api_view, authentication_classes, permission_classes
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Shipment, BananaImage, DeliveryPerson
from .serializers import ShipmentSerializer, DeliveryPersonSerializer
from .utils import get_optimized_route
from ml.utils import predict_banana_ripeness


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_post(request):
    return Response({"message": "POST request successful"})


class DeliveryPersonViewSet(viewsets.ModelViewSet):
    """
    Standard CRUD for delivery persons.
    """
    queryset = DeliveryPerson.objects.all().order_by('id')
    serializer_class = DeliveryPersonSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # optional override, or remove entirely to use default behavior
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dp = serializer.save()
        out = self.get_serializer(dp)
        headers = self.get_success_headers(out.data)
        return Response(out.data, status=status.HTTP_201_CREATED, headers=headers)


class ShipmentViewSet(viewsets.ModelViewSet):
    """
    CRUD + custom actions for banana shipments.
     - lookup_value_regex: only match numeric IDs, so that
       /delivery-persons/ isn’t swallowed by this detail route.
    """
    lookup_value_regex = r'\d+'
    queryset = Shipment.objects.all().order_by('-created_at')
    serializer_class = ShipmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(
        detail=True,
        methods=["post"],
        parser_classes=[MultiPartParser, FormParser],
        permission_classes=[AllowAny],
    )
    def upload_image(self, request, pk=None):
        shipment = self.get_object()
        img = request.FILES.get('image')
        if not img:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
            for chunk in img.chunks():
                tmp.write(chunk)
            tmp.flush()
            path = tmp.name

        out, b64 = predict_banana_ripeness(path, settings.WEIGHTS_PATH, settings.MAPPING_PATH)
        shipment.ripeness_summary   = out['ripeness']
        shipment.predictions        = out['predictions']
        shipment.dominant_ripeness  = out['dominant_ripeness']
        shipment.shelf_life         = out['shelf_life']
        shipment.result_image       = b64
        shipment.save()

        BananaImage.objects.create(shipment=shipment, image_data=img.read())
        return Response(out)

    @action(detail=True, methods=["post"], url_path='update_location')
    def update_location(self, request, pk=None):
        shipment = self.get_object()
        lat = request.data.get('latitude')
        lon = request.data.get('longitude')
        if lat is None or lon is None:
            return Response({'error': 'latitude and longitude are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        shipment.current_lat = float(lat)
        shipment.current_lon = float(lon)

        if request.data.get('optimized_route'):
            shipment.optimized_route = request.data['optimized_route']
            shipment.save()
            return Response(self.get_serializer(shipment).data)

        return self.compute_route(request, pk)

    @action(detail=True, methods=["post"], url_path='compute_route')
    def compute_route(self, request, pk=None):
        shipment = self.get_object()
        route = get_optimized_route(shipment.origin, shipment.destination)
        shipment.optimized_route = route
        shipment.save()
        return Response({'optimized_route': route})

    @action(detail=True, methods=["post"], url_path='update_status')
    def update_status(self, request, pk=None):
        shipment = self.get_object()
        new_status = request.data.get('status')
        valid = [c[0] for c in Shipment.STATUS_CHOICES]
        if new_status not in valid:
            return Response({'error': f'status must be one of {valid}'},
                            status=status.HTTP_400_BAD_REQUEST)
        shipment.status = new_status
        shipment.save()
        return Response(self.get_serializer(shipment).data)

    @action(detail=True, methods=['post'], url_path='assign_delivery')
    def assign_delivery(self, request, pk=None):
        shipment = self.get_object()
        raw_dp = request.data.get('delivery_person_id')
        try:
            dp_id = int(raw_dp)
        except (TypeError, ValueError):
            return Response({'error': 'delivery_person_id must be an integer.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            dp = DeliveryPerson.objects.get(id=dp_id)
        except DeliveryPerson.DoesNotExist:
            return Response({'error': 'DeliveryPerson not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        shipment.delivery_person = dp
        shipment.status = 'IN_TRANSIT'
        shipment.save()
        return Response(self.get_serializer(shipment).data)

    @action(detail=True, methods=["post"], url_path='mark_delivered')
    def mark_delivered(self, request, pk=None):
        shipment = self.get_object()
        shipment.status = 'DELIVERED'
        shipment.save()
        return Response(self.get_serializer(shipment).data)
