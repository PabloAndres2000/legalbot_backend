from rest_framework import serializers

from legalbot.apps.business import services as business_services
from legalbot.apps.users.api.serializers.group import GroupSerializer
from legalbot.apps.users.models import Partner
from legalbot.apps.users.providers import partner as partner_providers
from legalbot.apps.users.providers import user as user_providers


class PartnerListSerializer(serializers.ModelSerializer):
    identification_number = serializers.CharField(source="user.identification_number")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    business_name = serializers.ReadOnlyField(source="business.name")

    group = GroupSerializer(many=True, read_only=True, source="user.groups")

    class Meta:
        model = Partner
        fields = [
            "uuid",
            "business",
            "business_name",
            "identification_number",
            "first_name",
            "last_name",
            "address",
            "participation",
            "is_active",
            "group",
        ]


class CreatePartnerSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=user_providers.get_all_users())
    business = serializers.PrimaryKeyRelatedField(
        queryset=business_services.get_all_business()
    )
    address = serializers.CharField(max_length=200)
    participation = serializers.IntegerField(default=0)

    def validate(self, attrs):
        user = attrs["user"]
        business = attrs["business"]
        identification_number = user.identification_number

        if not identification_number:
            raise serializers.ValidationError("Identification number is required.")

        partner_already_exist = partner_providers.check_if_partner_already_exists(
            user_uuid=user, business_uuid=business, address=attrs["address"]
        )

        if partner_already_exist:
            raise serializers.ValidationError(
                "this partner is already associated with this business."
            )

        # Custom validation using the `get_partner_by_identification_number` function
        existing_partner_identification_number = (
            partner_providers.check_if_partner_identification_number_exist(
                identification_number=identification_number
            )
        )
        if existing_partner_identification_number:
            raise serializers.ValidationError(
                "A partner with this identification number already exists."
            )

        return attrs

    def create(self, validated_data):
        partner_providers.create_partner(
            user=validated_data["user"],
            business=validated_data["business"],
            address=validated_data["address"],
            participation=validated_data["participation"],
        )
        return validated_data
