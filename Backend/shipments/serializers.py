import tempfile
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Shipment, BananaImage, DeliveryPerson
from ml.utils import predict_banana_ripeness


class DateOnlyField(serializers.DateField):
    def to_representation(self, value):
        if hasattr(value, "date"):
            value = value.date()
        return super().to_representation(value)


class UserBriefSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "user_type"]

    def get_user_type(self, obj):
        return getattr(getattr(obj, "profile", None), "user_type", None)


class DeliveryPersonSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = UserBriefSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = DeliveryPerson
        fields = ["id", "user", "user_id", "phone_number", "vehicle_info"]


class BananaImageSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = BananaImage
        fields = ["id", "uploaded_at"]


class ShipmentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    shipment_date     = DateOnlyField()
    estimated_arrival = DateOnlyField(allow_null=True)

    created_by       = UserBriefSerializer(read_only=True)
    receiver         = UserBriefSerializer(read_only=True)
    created_by_id    = serializers.IntegerField(write_only=True)
    receiver_id      = serializers.IntegerField(write_only=True)

    delivery_person      = DeliveryPersonSerializer(read_only=True)
    delivery_person_id   = serializers.CharField(write_only=True, required=False)

    ripeness_summary  = serializers.JSONField(read_only=True)
    optimized_route   = serializers.JSONField(read_only=True)
    map_url           = serializers.CharField(read_only=True)

    images            = BananaImageSerializer(many=True, read_only=True)
    image             = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Shipment
        fields = [
            "id", "created_by", "created_by_id",
            "receiver", "receiver_id",
            "delivery_person", "delivery_person_id",
            "origin", "destination", "quantity", "status",
            "shipment_date", "estimated_arrival",
            "ripeness_summary", "dominant_ripeness",
            "shelf_life", "result_image",
            "current_lat", "current_lon", "optimized_route", "map_url",
            "created_at", "last_updated", "images", "image",
        ]
        read_only_fields = ["id", "created_at", "last_updated", "alert_sent"]

    def _dump_to_temp(self, file_obj):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
            for chunk in file_obj.chunks():
                tmp.write(chunk)
            tmp.flush()
            return tmp.name

    def _run_prediction(self, tmp_path):
        request = self.context.get('request')
        weights = getattr(request.settings, 'WEIGHTS_PATH', None)
        mapping = getattr(request.settings, 'MAPPING_PATH', None)
        return predict_banana_ripeness(tmp_path, weights, mapping)

    def create(self, validated_data):
        image_file = validated_data.pop('image', None)
        cb = User.objects.get(id=validated_data.pop('created_by_id'))
        rc = User.objects.get(id=validated_data.pop('receiver_id'))
        dp_id = validated_data.pop('delivery_person_id', None)

        if image_file:
            tmp_path = self._dump_to_temp(image_file)
            output, img_b64 = self._run_prediction(tmp_path)
            validated_data.update({
                'ripeness_summary': output['ripeness'],
                'dominant_ripeness': output['dominant_ripeness'],
                'shelf_life': output['shelf_life'],
                'result_image': img_b64,
            })

        shipment = Shipment.objects.create(
            created_by=cb, receiver=rc, **validated_data
        )

        if dp_id:
            shipment.delivery_person_id = int(dp_id)
            shipment.status = 'IN_TRANSIT'
            shipment.save()

        if image_file:
            BananaImage.objects.create(
                shipment=shipment,
                image_data=image_file.read()
            )
        return shipment

    def update(self, instance, validated_data):
        image_file = validated_data.pop('image', None)
        dp_id = validated_data.pop('delivery_person_id', None)
        instance = super().update(instance, validated_data)

        if dp_id is not None:
            instance.delivery_person_id = int(dp_id)
            instance.status = 'IN_TRANSIT'
            instance.save()

        if image_file:
            tmp_path = self._dump_to_temp(image_file)
            output, img_b64 = self._run_prediction(tmp_path)
            Shipment.objects.filter(pk=instance.pk).update(
                ripeness_summary=output['ripeness'],
                dominant_ripeness=output['dominant_ripeness'],
                shelf_life=output['shelf_life'],
                result_image=img_b64,
            )
            BananaImage.objects.create(
                shipment=instance,
                image_data=image_file.read()
            )
        return instance
