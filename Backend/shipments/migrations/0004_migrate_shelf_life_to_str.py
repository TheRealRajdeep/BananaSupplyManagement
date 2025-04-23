from django.db import migrations

def convert_shelf_life(apps, schema_editor):
    Shipment = apps.get_model('shipments', 'Shipment')
    for obj in Shipment.objects.all():
        obj.shelf_life = str(obj.shelf_life)
        obj.save()

class Migration(migrations.Migration):
    dependencies = [
        ('shipments', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(convert_shelf_life, migrations.RunPython.noop),
    ]
