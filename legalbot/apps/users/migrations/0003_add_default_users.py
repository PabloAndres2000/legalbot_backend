from django.db import migrations
from django.contrib.auth.models import Group
from legalbot.apps.users.models import User


def create_default_users(apps, schema_editor):
    User.objects.create_superuser(
        identification_number='12.432.567-K',
        first_name='Miguel González',
        last_name='González',
        password='miguel',
    )
    User.objects.create_superuser(
        identification_number='10.456.983-9',
        first_name='esteban lopez',
        last_name='lopez',
        password='esteban',
    )
    User.objects.create(
        uuid='32f5073d-2c2c-4dfe-a09d-3ee3a3a18ff1',
        identification_number='15.192.932-6',
        first_name='juan garcia',
        last_name='garcia',
        password='juan',
    )
    admin_group = Group.objects.get(name='admin')
    partner_group = Group.objects.get(name='partner')

    miguel_user = User.objects.get(identification_number='12.432.567-K')
    esteban_user = User.objects.get(identification_number='10.456.983-9')

    miguel_user.uuid = '4244b0ea-edc4-4c8f-a4f8-3e5b95a45ba3'
    miguel_user.save()

    esteban_user.uuid = '5abb8658-996b-40d2-aa80-0d90592796e5'
    esteban_user.save()

    miguel_user.groups.add(admin_group)
    esteban_user.groups.add(admin_group)

    juan_user = User.objects.get(identification_number='15.192.932-6')

    juan_user.groups.add(partner_group)


class Migration(migrations.Migration):

    dependencies = [
        # Add the dependency on the previous migration
        ('users', '0002_add_default_groups'),
    ]

    operations = [
        migrations.RunPython(create_default_users),
    ]
