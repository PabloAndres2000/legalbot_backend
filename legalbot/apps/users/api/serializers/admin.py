from rest_framework import serializers

from legalbot.apps.business import services as business_services
from legalbot.apps.business import services as faculties_services
from legalbot.apps.business.api.serializers.faculty import FacultyListSerializer
from legalbot.apps.users.api.serializers.group import GroupSerializer
from legalbot.apps.users.models import Administrator
from legalbot.apps.users.providers import admin as admin_providers
from legalbot.apps.users.providers import user as user_providers


class AdministratorListSerializer(serializers.ModelSerializer):
    business_name = serializers.ReadOnlyField(source="business.name")
    first_name = serializers.ReadOnlyField(source="user.first_name")
    identification_number = serializers.CharField(source="user.identification_number")

    group = GroupSerializer(many=True, read_only=True, source="user.groups")
    faculties = FacultyListSerializer(many=True, read_only=True)

    class Meta:
        model = Administrator
        fields = [
            "uuid",
            "business",
            "business_name",
            "user",
            "first_name",
            "identification_number",
            "faculties",
            "group",
        ]


class CreateAdminSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=user_providers.get_all_users())
    business = serializers.PrimaryKeyRelatedField(
        queryset=business_services.get_all_business()
    )
    faculties = serializers.PrimaryKeyRelatedField(
        queryset=faculties_services.get_all_faculties(), many=True, required=False
    )

    def validate(self, attrs):
        user = attrs["user"]
        business = attrs["business"]
        identification_number = user.identification_number

        admin_already_exist = admin_providers.check_if_admin_already_exists(
            user_uuid=user, business_uuid=business
        )

        if admin_already_exist:
            raise serializers.ValidationError(
                "this admin is already associated with this business."
            )

        # Perform your custom validation here
        if not identification_number:
            raise serializers.ValidationError("Identification number is required.")

        # Custom validation using the `get_partner_by_identification_number` function
        existing_admin = admin_providers.check_if_admin_identification_number_exist(
            identification_number=identification_number
        )
        if existing_admin:
            raise serializers.ValidationError(
                "A admin with this identification number already exists."
            )

        return attrs

    def create(self, validated_data):
        faculties = validated_data.pop("faculties", [])

        admin = admin_providers.create_admin(
            user=validated_data["user"],
            business=validated_data["business"],
        )
        admin.faculties.set(faculties)  # Assign faculties using set() method
        return admin
