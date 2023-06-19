from rest_framework import serializers

from legalbot.apps.business.models import Business
from legalbot.apps.business.providers import business as business_providers
from legalbot.apps.users.api.serializers.admin import AdministratorListSerializer
from legalbot.apps.users.api.serializers.partner import PartnerListSerializer


class UserOwnedBusinessesSerializer(serializers.ModelSerializer):
    partners = serializers.SerializerMethodField()
    admins = serializers.SerializerMethodField()

    class Meta:
        model = Business
        fields = [
            "uuid",
            "name",
            "identification_number",
            "is_active",
            "partners",
            "admins",
        ]

    def get_partners(self, obj):
        partners = obj.partners.filter(user__identification_number=self.context["rut"])
        serializer = PartnerListSerializer(partners, many=True)
        return serializer.data

    def get_admins(self, obj):
        admins = obj.administrators.filter(
            user__identification_number=self.context["rut"]
        )
        serializer = AdministratorListSerializer(admins, many=True)
        return serializer.data


class BusinessListSerializer(serializers.ModelSerializer):
    partners = PartnerListSerializer(many=True, read_only=True)
    admins = AdministratorListSerializer(
        source="administrators", many=True, read_only=True
    )

    class Meta:
        model = Business
        fields = [
            "uuid",
            "name",
            "identification_number",
            "is_active",
            "partners",
            "admins",
        ]


class CreateBusinessSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    identification_number = serializers.CharField(max_length=13, required=True)

    def validate(self, attrs):
        name = attrs["name"]
        identification_number = attrs["identification_number"]

        if not name:
            raise serializers.ValidationError("name is required.")

        if not identification_number:
            raise serializers.ValidationError("Identification number is required.")

        existing_business_identification_number = (
            business_providers.check_if_business_identification_number_exist(
                identification_number=identification_number
            )
        )

        existing_business_name = business_providers.check_if_business_name_exist(
            name=name
        )

        if existing_business_name:
            raise serializers.ValidationError(
                "A business with this name already exists."
            )

        if existing_business_identification_number:
            raise serializers.ValidationError(
                "A business with this identification number already exists."
            )

        return attrs

    def create(self, validated_data):
        business_providers.create_partner(
            name=validated_data["name"],
            identification_number=validated_data["identification_number"],
        )
        return validated_data


class PartnerAdministratorSerializer(serializers.Serializer):
    partners = PartnerListSerializer(many=True)
    administrators = AdministratorListSerializer(many=True)
