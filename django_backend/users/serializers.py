from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Card
        fields = ['id', 'card_type', 'masked_card', 'last_four', 'created_at', 'card_number']
        read_only_fields = ['masked_card', 'last_four', 'created_at']

    def create(self, validated_data):
        card_number = validated_data.pop('card_number')
        if not card_number.isdigit() or len(card_number) < 12:
            raise serializers.ValidationError("Invalid card number")

        validated_data['last_four'] = card_number[-4:]
        validated_data['masked_card'] = "**** **** **** " + card_number[-4:]
        return Card.objects.create(**validated_data)
