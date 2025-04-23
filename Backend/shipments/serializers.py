# shipments/serializers.py
import tempfile
import datetime
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User
from .models import Shipment, BananaImage
from ml.utils import predict_banana_ripeness

class DateOnlyField(serializers.DateField):
    """
    A DateField that will happily accept a datetime by dropping the time portion.
    """
    def to_representation(self, value):
        if isinstance(value, datetime.datetime):
            value = value.date()
        return super().to_representation(value)

class UserBriefSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'user_type']

    def get_user_type(self, obj):
        return getattr(getattr(obj, 'profile', None), 'user_type', None)


class BananaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BananaImage
        fields = ['id', 'uploaded_at']


class ShipmentSerializer(serializers.ModelSerializer):
    # Use our DateOnlyField for date columns
    shipment_date     = DateOnlyField()
    estimated_arrival = DateOnlyField(allow_null=True)

    created_by        = UserBriefSerializer(read_only=True)
    receiver          = UserBriefSerializer(read_only=True)
    created_by_id     = serializers.IntegerField(write_only=True)
    receiver_id       = serializers.IntegerField(write_only=True)
    images            = BananaImageSerializer(many=True, read_only=True)
    image             = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Shipment
        fields = [
            'id', 'created_by', 'receiver', 'created_by_id', 'receiver_id',
            'origin', 'destination', 'quantity', 'status',
            'shipment_date', 'estimated_arrival',
            'ripeness_status', 'dominant_ripeness', 'ripeness_summary',
            'shelf_life', 'result_image',
            'current_lat', 'current_lon', 'optimized_route',
            'created_at', 'last_updated', 'images', 'image'
        ]
        read_only_fields = ['id', 'created_at', 'last_updated', 'alert_sent']

    def _dump_to_temp(self, in_memory_file):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
            for chunk in in_memory_file.chunks():
                tmp.write(chunk)
            tmp.flush()
            return tmp.name

    def _run_prediction(self, tmp_path):
        weights = getattr(settings, 'WEIGHTS_PATH', '/absolute/path/to/best.pt')
        mapping = getattr(settings, 'MAPPING_PATH', '/absolute/path/to/data.yaml')
        return predict_banana_ripeness(tmp_path, weights, mapping)

    def create(self, validated_data):
        image_file = validated_data.pop('image', None)
        cb = User.objects.get(id=validated_data.pop('created_by_id'))
        rc = User.objects.get(id=validated_data.pop('receiver_id'))

        # If there's an image, run prediction first
        if image_file:
            tmp_path = self._dump_to_temp(image_file)
            output, img_b64 = self._run_prediction(tmp_path)
            validated_data.update({
                'ripeness_summary':  output['ripeness'],
                'dominant_ripeness':  output['dominant_ripeness'],
                'shelf_life':         output['shelf_life'],
                'result_image':       img_b64
            })

        shipment = Shipment.objects.create(
            created_by=cb,
            receiver=rc,
            **validated_data
        )

        if image_file:
            BananaImage.objects.create(
                shipment=shipment,
                image_data=image_file.read()
            )

        return shipment

    def update(self, instance, validated_data):
        image_file = validated_data.pop('image', None)
        instance = super().update(instance, validated_data)

        if image_file:
            tmp_path = self._dump_to_temp(image_file)
            output, img_b64 = self._run_prediction(tmp_path)
            # update only the lightweight fields
            Shipment.objects.filter(pk=instance.pk).update(
                ripeness_summary=output['ripeness'],
                dominant_ripeness=output['dominant_ripeness'],
                shelf_life=output['shelf_life'],
                result_image=img_b64
            )
            BananaImage.objects.create(
                shipment=instance,
                image_data=image_file.read()
            )

        return instance
