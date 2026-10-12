
from django.db import models


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="INR")
    status = models.CharField(max_length=20, default="PENDING")
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "transactions"

    def __str__(self):
        return f"Transaction {self.id} - {self.status}"