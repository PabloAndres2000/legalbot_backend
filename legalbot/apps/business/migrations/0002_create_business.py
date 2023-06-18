from django.db import migrations
from legalbot.apps.business.models import Business


def create_business(apps, schema_editor):
    Business.objects.create(
        name="LegalbotSPA",
        identification_number="76.192.448-K",
    )


class Migration(migrations.Migration):
    dependencies = [
        # Add the dependency on the previous migration
        ("business", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_business),
    ]
