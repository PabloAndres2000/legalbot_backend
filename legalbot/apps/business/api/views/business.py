from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_access_policy import AccessPolicy

from legalbot.apps.business.api.serializers.business import (
    BusinessListSerializer,
    CreateBusinessSerializer,
    PartnerAdministratorSerializer,
    UserOwnedBusinessesSerializer,
)
from legalbot.apps.business.providers import business as business_providers
from legalbot.utils.constants import DATA_NOT_FOUND, TRY_AGAIN_LATER


class BusinessAccessPolicy(AccessPolicy):
    """
    Access policy for the BusinessViewSet
    """

    statements = [
        {
            "action": ["create_business"],
            "principal": ["group:admin"],
            "effect": "allow",
        },
        {
            "action": ["delete_business"],
            "principal": ["group:admin"],
            "effect": "allow",
        },
        {
            "action": ["get_businesses_with_partner_or_admin_by_rut"],
            "principal": ["group:admin"],
            "effect": "allow",
        },
        {
            "action": ["get_partners_admins_by_rut"],
            "principal": ["group:admin"],
            "effect": "allow",
        },
    ]


class BusinessPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class BusinessViewSet(viewsets.ViewSet):
    pagination_class = BusinessPagination
    permission_classes = (BusinessAccessPolicy,)

    # POST: api/business/create_buiness/
    @action(
        detail=False,
        methods=["post"],
        url_name="create-business",
        url_path="create_business",
    )
    def create_business(self, request):
        serializer = CreateBusinessSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data={"detail": "Business created successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={"detail": TRY_AGAIN_LATER},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # DELETE: api/business/<uuid>/delete_business/
    @action(
        detail=True,
        methods=["delete"],
        url_name="delete-business",
        url_path="delete_business",
    )
    def delete_business(self, request, pk):
        business = business_providers.get_business_by_uuid(uuid=pk)
        if not business:
            return Response({"message": DATA_NOT_FOUND})
        serializer = BusinessListSerializer(business)
        business.delete()

        return Response(serializer.data, status=204)

    # GET: api/business/get_businesses_with_partner_or_admin_by_rut/?rut=
    @action(
        detail=False,
        methods=["get"],
        url_name="get-business-by-rut",
        url_path="get_businesses_with_partner_or_admin_by_rut",
    )
    def get_businesses_with_partner_or_admin_by_rut(self, request):
        rut = request.GET.get("rut")
        business = business_providers.get_business_by_manager_or_partner_id_number(
            identification_number=rut
        )
        if not business:
            return Response(
                {
                    "message": "This RUT cannot be found to see which company the partner or administrator belongs to."
                }
            )

        paginator = self.pagination_class()
        paginated_business = paginator.paginate_queryset(business, request)
        serializer = UserOwnedBusinessesSerializer(
            paginated_business, many=True, context={"rut": rut}
        )
        return paginator.get_paginated_response(serializer.data)

    # GET: api/business/get_partners_admins_by_rut/?rut=
    @action(
        detail=False,
        methods=["get"],
        url_name="get-partners-admins-by-rut",
        url_path="get_partners_admins_by_rut",
    )
    def get_partners_admins_by_rut(self, request):
        rut = request.GET.get("rut")
        if not rut:
            return Response(DATA_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        business = business_providers.get_business_by_identification_number(
            identification_number=rut
        )

        if not business:
            return Response({"message": "No business found for the provided RUT."})
        partners = business.partners.prefetch_related("user")
        administrators = business.administrators.prefetch_related("user")

        paginator = self.pagination_class()
        paginated_partners = paginator.paginate_queryset(partners, request)
        paginated_administrators = paginator.paginate_queryset(administrators, request)

        serializer = PartnerAdministratorSerializer(
            {"partners": paginated_partners, "administrators": paginated_administrators}
        )

        return paginator.get_paginated_response(serializer.data)
