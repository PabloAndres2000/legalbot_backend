from django.urls import path
from rest_framework import routers

from legalbot.apps.business.api.views.business import BusinessViewSet
from legalbot.apps.users.api.views.admin import AdminViewSet
from legalbot.apps.users.api.views.partner import PartnerViewSet
from legalbot.apps.users.api.views.user import UserViewSet

router = routers.SimpleRouter()

router.register(r"partners", PartnerViewSet, basename="partners")
router.register(r"admins", AdminViewSet, basename="admins")
router.register(r"business", BusinessViewSet, basename="business")
router.register(r"users", UserViewSet, basename="users")


urlpatterns = router.urls
