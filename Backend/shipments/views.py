# shipments/views.py
import tempfile
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings

from .models import Shipment, BananaImage
from .serializers import ShipmentSerializer
from ml.utils import predict_banana_ripeness

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all().order_by('-created_at')
    serializer_class = ShipmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=True,
        methods=['post'],
        parser_classes=[MultiPartParser, FormParser],
        permission_classes=[AllowAny]    # or IsAuthenticated if you want auth here
    )
    def upload_image(self, request, pk=None):
        shipment = self.get_object()
        img_file = request.FILES.get('image')
        if not img_file:
            return Response({'error': 'No image provided'}, status=400)
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        for chunk in img_file.chunks(): tmp.write(chunk)
        tmp.flush()
        output, img_b64 = predict_banana_ripeness(tmp.name, settings.WEIGHTS_PATH, settings.MAPPING_PATH)
        shipment.ripeness_summary  = output['ripeness']
        shipment.predictions        = output['predictions']
        shipment.dominant_ripeness  = output['dominant_ripeness']
        shipment.shelf_life         = output['shelf_life']
        shipment.result_image       = img_b64
        shipment.save()
        BananaImage.objects.create(shipment=shipment, image_data=img_file.read())
        return Response(output)