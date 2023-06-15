from celery import shared_task
from django.db import IntegrityError

from legalbot.apps.users.models import Partner
from legalbot.apps.users.providers import partner as partner_providers
from legalbot.apps.users.providers import user as user_providers


@shared_task
def create_partner_task(
    user_uuid: str, business_uuid: str, address: str, participation: int
):
    try:
        partner = Partner.objects.create(
            user=user_uuid,
            business_id=business_uuid,
            address=address,
            participation=participation,
        )
        user_providers.add_group_to_user(user=partner.user, group_name="partner")
        return partner
    except IntegrityError:
        raise Exception("Error creating partner: IntegrityError")
