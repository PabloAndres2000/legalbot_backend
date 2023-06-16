from django.db import migrations
from legalbot.apps.business.models import Faculty


def create_faculties(apps, schema_editor):

    faculties_name = ["Abrir cuentas corrientes",
                      "Firmar contratos de compraventa", "Firmar cheques"]
    for name in faculties_name:
        Faculty.objects.create(
            name=name,
        )


class Migration(migrations.Migration):

    dependencies = [
        # Add the dependency on the previous migration
        ('business', '0002_create_business'),
    ]

    operations = [
        migrations.RunPython(create_faculties),
    ]
