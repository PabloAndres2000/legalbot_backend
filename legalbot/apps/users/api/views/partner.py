from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_access_policy import AccessPolicy

from legalbot.apps.users.api.serializers.partner import CreatePartnerSerializer
from legalbot.utils.constants import TRY_AGAIN_LATER


class PartnerAccessPolicy(AccessPolicy):
    """
    Access policy for the AdminViewSet
    """

    statements = [
        {"action": ["create_partner"], "principal": ["group:admin"], "effect": "allow"}
    ]


class PartnerViewSet(viewsets.ViewSet):
    # POST: api/partners/create_partner/
    permission_classes = (PartnerAccessPolicy,)

    @action(
        detail=False,
        methods=["post"],
        url_name="create-partner",
        url_path="create_partner",
    )
    def create_partner(self, request):
        serializer = CreatePartnerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data={"detail": "Partner created successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={"detail": TRY_AGAIN_LATER},
            status=status.HTTP_400_BAD_REQUEST,
        )
