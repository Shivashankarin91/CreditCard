
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Card
from .serializers import CardSerializer, AddCardSerializer


class CardListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cards = Card.objects.filter(user=request.user).order_by("-created_at")
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        card_number = data.pop("card_number")

        # Keep only the last four digits.
        last_four = card_number[-4:]
        del card_number

        card = Card.objects.create(
            user=request.user,
            cardholder_name=data["cardholder_name"],
            card_type=data["card_type"],
            last_four_digits=last_four,
            expiry_month=data["expiry_month"],
            expiry_year=data["expiry_year"],
        )

        return Response(
            CardSerializer(card).data,
            status=status.HTTP_201_CREATED,
        )


class CardDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)
