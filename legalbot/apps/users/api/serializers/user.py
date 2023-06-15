from rest_framework import serializers

from legalbot.apps.users.models import User
from legalbot.apps.users.providers import user as user_providers


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uuid",
            "first_name",
            "last_name",
            "identification_number",
            "is_staff",
            "created_at",
            "updated_at",
            "is_active",
        ]


class UserSignUpSerializer(serializers.Serializer):
    """
    User sign up serializer.
    """

    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    identification_number = serializers.CharField(max_length=12, required=True)
    password = serializers.CharField(min_length=5, required=True)

    def validate(self, attrs):
        identification_number = attrs["identification_number"]

        if not identification_number:
            raise serializers.ValidationError("Identification number is required.")

        existing_user = user_providers.check_if_user_identification_number_exist(
            identification_number=identification_number
        )
        if existing_user:
            raise serializers.ValidationError(
                "A User with this identification number already exists."
            )

        return attrs

    def create(self, validated_data):
        user = user_providers.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            identification_number=validated_data["identification_number"],
            ip_address=self.context.get("ip_address"),
            password=validated_data["password"],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(min_length=5, required=True)

    def validate(self, attrs):
        identification_number = attrs["identification_number"]
        password = attrs["password"]

        if not identification_number:
            raise serializers.ValidationError("Identification number is required.")

        if not password:
            raise serializers.ValidationError("password is required.")

    def create(self, validated_data):
        user = user_providers.login(
            email=validated_data["email"],
            ip_address=self.context.get("ip_address"),
            password=validated_data["password"],
        )
        return user


class UpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    identification_number = serializers.CharField(max_length=20, required=False)

    def validate(self, attrs):
        instance = getattr(self, "instance", None)
        same_identification_number = instance.identification_number == attrs.get(
            "identification_number"
        )

        existing_user = user_providers.check_if_user_identification_number_exist(
            identification_number=attrs.get("identification_number")
        )
        if existing_user and not same_identification_number:
            raise serializers.ValidationError(
                "A User with this identification number already exists."
            )

        return attrs

    def update(self, instance, validated_data):
        user = user_providers.update_user_by_uuid(
            user_uuid=int(instance.uuid), **validated_data
        )
        return user


class UpdatePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=255)

    class Meta:
        model = User
        fields = [
            "uuid",
            "password",
        ]

    def update(self, instance, validated_data):
        user = user_providers.update_password_by_uuid(
            uuid=str(instance.uuid), password=validated_data["password"]
        )
        return user
