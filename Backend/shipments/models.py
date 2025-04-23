# shipments/models.py
from djongo import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import re
from django.db import transaction

class Shipment(models.Model):
    RIPENESS_STATES = (
        ('unripe', 'Unripe'),
        ('freshripe', 'Fresh Ripe'),
        ('ripe', 'Ripe'),
        ('overripe', 'Overripe'),
        ('Unknown', 'Unknown')
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled')
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_shipments')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_shipments')
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    shipment_date = models.DateField(default=timezone.now)
    estimated_arrival = models.DateField(null=True, blank=True)

    ripeness_status = models.CharField(max_length=50, choices=RIPENESS_STATES, default='Unknown')
    dominant_ripeness = models.CharField(max_length=50, choices=RIPENESS_STATES, default='Unknown')
    ripeness_summary = models.JSONField(default=dict, blank=True)
    predictions = models.JSONField(default=list, blank=True)
    shelf_life = models.CharField(max_length=20, blank=True)
    alert_sent = models.BooleanField(default=False)
    result_image = models.TextField(blank=True)

    current_lat = models.FloatField(null=True, blank=True)
    current_lon = models.FloatField(null=True, blank=True)
    optimized_route = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipment {self.id} from {self.origin} to {self.destination}"

    def estimated_expiry_date(self):
        # shelf_life is a string like "4-6 days"; expiry calculation omitted
        return None

class BananaImage(models.Model):
    shipment = models.ForeignKey(Shipment, related_name='images', on_delete=models.CASCADE)
    image_data = models.BinaryField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Shipment {self.shipment.id}"

@receiver(post_save, sender=Shipment)
def check_shipment_shelf_life(sender, instance, **kwargs):
    # if instance.shelf_life and not instance.alert_sent:
    #     # parse number of days from shelf_life, e.g. "4-6 days" -> 4
    #     try:
    #         days = int(instance.shelf_life.split('-')[0])
    #     except:
    #         days = 0
    #     if days <= 3 :
    #         subj = f"ALERT: Shipment #{instance.id} nearing expiry"
    #         msg = f"Your shipment #{instance.id} has ~{instance.shelf_life} remaining."
    #         send_mail(subj, msg, settings.EMAIL_HOST_USER, [instance.receiver.email], fail_silently=False)
    #         instance.alert_sent = True
    #         instance.save(update_fields=['alert_sent'])
    # only act on updates, not on the initial create
    if instance.alert_sent or not instance.shelf_life:
        return

    # pull out the first number in shelf_life
    m = re.search(r'(\d+)', instance.shelf_life)
    if not m:
        # nothing to do if no numeric shelf life
        return

    days = int(m.group(1))
    if days > 3:
        return

    # send the alert
    subject = f"ALERT: Shipment #{instance.id} nearing expiry"
    message = f"Your shipment #{instance.id} has ~{instance.shelf_life} remaining."
    try:
        send_mail(subject,
                  message,
                  settings.DEFAULT_FROM_EMAIL,
                  [instance.receiver.email],
                  fail_silently=False)
    except Exception as e:
        # log it and give up
        import logging
        logging.getLogger(__name__).error(f"Failed to send expiry alert: {e}")
        return

    # **update alert_sent without retriggering post_save**
    Shipment.objects.filter(pk=instance.pk).update(alert_sent=True)