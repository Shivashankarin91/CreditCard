from django.db import models
from django.conf import settings

class Card(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cards")
    card_type = models.CharField(max_length=10, choices=[("Credit", "Credit"), ("Debit", "Debit")])
    masked_card = models.CharField(max_length=19)  # e.g., **** **** **** 1234
    last_four = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_type} Card ending with {self.last_four}"