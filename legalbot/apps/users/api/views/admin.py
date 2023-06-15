from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_access_policy import AccessPolicy

from legalbot.apps.users.api.serializers.admin import CreateAdminSerializer
from legalbot.utils.constants import TRY_AGAIN_LATER


class AdminAccessPolicy(AccessPolicy):
    """
    Access policy for the AdminViewSet
    """

    statements = [
        {"action": ["create_admin"], "principal": ["group:admin"], "effect": "allow"}
    ]


class AdminViewSet(viewsets.ViewSet):
    # POST: api/admins/create_admin/
    permission_classes = (AdminAccessPolicy,)

    @action(
        detail=False, methods=["post"], url_name="create-admin", url_path="create_admin"
    )
    def create_admin(self, request):
        serializer = CreateAdminSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data={"detail": "Admin created successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={"detail": TRY_AGAIN_LATER},
            status=status.HTTP_400_BAD_REQUEST,
        )
