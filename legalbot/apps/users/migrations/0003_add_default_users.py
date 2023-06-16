from django.db import migrations
from django.contrib.auth.models import Group
from legalbot.apps.users.models import User


def create_default_users(apps, schema_editor):
    miguel_user = User.objects.create_superuser(
        identification_number='12432567-K',
        first_name='Miguel González',
        last_name='González',
        password='miguel',
    )
    esteban_user = User.objects.create_superuser(
        identification_number='10456983-9',
        first_name='esteban lopez',
        last_name='lopez',
        password='esteban',
    )
    miguel_user.uuid = '4244b0ea-edc4-4c8f-a4f8-3e5b95a45ba3'
    miguel_user.save()

    esteban_user.uuid = '5abb8658-996b-40d2-aa80-0d90592796e5'
    esteban_user.save()

    juan_user = User.objects.create(
        uuid='5abb8658-996b-40d2-aa80-0d90592796e5',
        identification_number='15192932-6',
        first_name='juan garcia',
        last_name='garcia',
        password='juan',
    )
    admin_group = Group.objects.get(name='admin')
    partner_group = Group.objects.get(name='partner')

    miguel_user.groups.add(admin_group)
    esteban_user.groups.add(admin_group)
    juan_user.groups.add(partner_group)


class Migration(migrations.Migration):

    dependencies = [
        # Add the dependency on the previous migration
        ('users', '0002_add_default_groups'),
    ]

    operations = [
        migrations.RunPython(create_default_users),
    ]
