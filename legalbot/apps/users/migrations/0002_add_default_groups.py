from django.db import migrations, transaction


@transaction.atomic
def create_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.create(name="admin")
    Group.objects.create(name="partner")


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(code=create_group),
    ]
