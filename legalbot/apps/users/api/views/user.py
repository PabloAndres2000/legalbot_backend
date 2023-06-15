from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_access_policy import AccessPolicy

from legalbot.apps.users.api.serializers.user import (
    UpdatePasswordSerializer,
    UpdateSerializer,
    UserListSerializer,
    UserSignUpSerializer,
)
from legalbot.apps.users.providers import token as token_providers
from legalbot.apps.users.providers import user as user_providers
from legalbot.apps.users.utils.ip import get_client_ip
from legalbot.utils.constants import (
    DATA_NOT_FOUND,
    NOT_FILLED_FIELDS,
    PERMISSIONS_ERROR,
    WRONG_CREDENTIALS,
)


class UserAccessPolicy(AccessPolicy):
    """
    Access policy for the UserViewSet
    """

    statements = [
        {"action": ["get_all_users"], "principal": ["group:admin"], "effect": "allow"},
        {"action": ["signup"], "principal": ["*"], "effect": "allow"},
        {"action": ["update_user"], "principal": ["group:admin"], "effect": "allow"},
        {
            "action": ["change_password"],
            "principal": ["group:admin"],
            "effect": "allow",
        },
        {
            "action": ["change_password"],
            "principal": ["group:admin"],
            "effect": "allow",
        },
        {"action": ["login"], "principal": ["*"], "effect": "allow"},
    ]


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UserViewSet(viewsets.ViewSet):
    pagination_class = UserPagination
    permission_classes = (UserAccessPolicy,)
    # GET: api/users/get_all_users/

    @action(
        detail=False,
        methods=["get"],
        url_name="get-all-users",
        url_path="get_all_users",
    )
    def get_all_users(self, request):
        users = user_providers.get_all_users()

        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)

        serializer = UserListSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

    # POST: api/users/signup/
    @action(detail=False, methods=["post"], url_name="signup", url_path="signup")
    def signup(self, request):
        context = {"ip_address": get_client_ip(request)}
        serializer = UserSignUpSerializer(data=request.data, context=context)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data={"message": "Usuario creado con exito"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT: api/users/<uuid>/update_user/
    @action(
        detail=True, methods=["put"], url_name="update-user", url_path="update_user"
    )
    def update_user(self, request, pk):
        if not pk:
            return Response(DATA_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if not user_providers.check_user_is_owner_or_staff(
            request_user=request.user, user_uuid=pk
        ):
            return Response(PERMISSIONS_ERROR, status=status.HTTP_403_FORBIDDEN)
        user = user_providers.get_user_by_uuid(uuid=pk)
        if not user:
            return Response(DATA_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"message": "Usuario actualizado con exito"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT: api/users/user/<uuid>/change_password
    @action(
        detail=True,
        methods=["put"],
        url_name="change-password",
        url_path="change_password",
    )
    def change_password(self, request, pk):
        if not pk:
            return Response(DATA_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        if not user_providers.check_user_is_owner_or_staff(
            request_user=request.user, user_uuid=pk
        ):
            return Response(PERMISSIONS_ERROR, status=status.HTTP_403_FORBIDDEN)
        user = user_providers.get_user_by_uuid(uuid=pk)
        if not user:
            return Response(DATA_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdatePasswordSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save(update_fields=["password", "updated_at"])
            token_providers.remove_token_by_user_uuid(user_uuid=str(user.uuid))
            return Response(
                data={"message": "Contraseña actualizada con exito"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # POST: api/users/login
    @action(detail=False, methods=["post"], url_name="login", url_path="login")
    def login(self, request):
        identification_number = request.data.get("identification_number")
        password = request.data.get("password")
        ip_address = get_client_ip(request=request)

        if not identification_number or not password:
            return Response(data=NOT_FILLED_FIELDS, status=status.HTTP_400_BAD_REQUEST)
        user, token = user_providers.login(
            identification_number=identification_number,
            password=password,
            ip_address=ip_address,
        )
        if not user or not token:
            return Response(data=WRONG_CREDENTIALS, status=status.HTTP_400_BAD_REQUEST)
        data = {"user": UserListSerializer(user).data, "access_token": token}
        return Response(data, status=status.HTTP_200_OK)
