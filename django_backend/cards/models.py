
from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):

    CARD_TYPES = [
        ("CREDIT", "Credit Card"),
        ("DEBIT", "Debit Card"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="saved_cards"
    )

    cardholder_name = models.CharField(max_length=100)

    card_type = models.CharField(
        max_length=10,
        choices=CARD_TYPES
    )

    last_four_digits = models.CharField(max_length=4)

    expiry_month = models.PositiveSmallIntegerField()
    expiry_year = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.card_type} ending in "
            f"{self.last_four_digits}"
        )

