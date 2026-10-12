
from datetime import date

from rest_framework import serializers

from .models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            "id",
            "cardholder_name",
            "card_type",
            "last_four_digits",
            "expiry_month",
            "expiry_year",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "last_four_digits",
            "created_at",
        ]


class AddCardSerializer(serializers.Serializer):
    cardholder_name = serializers.CharField(max_length=100)

    card_type = serializers.ChoiceField(
        choices=["CREDIT", "DEBIT"]
    )

    card_number = serializers.CharField(
        write_only=True,
        min_length=13,
        max_length=19,
        trim_whitespace=True,
    )

    expiry_month = serializers.IntegerField(min_value=1, max_value=12)
    expiry_year = serializers.IntegerField(min_value=2026, max_value=9999)

    def validate_card_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Card number must contain digits only."
            )
        return value

    def validate(self, attrs):
        today = date.today()
        month = attrs["expiry_month"]
        year = attrs["expiry_year"]

        if (year, month) < (today.year, today.month):
            raise serializers.ValidationError(
                {"expiry_month": "The card has expired."}
            )

        return attrs