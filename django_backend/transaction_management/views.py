
from datetime import date

from django.db.models import QuerySet
from django.utils.dateparse import parse_date
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer

from .models import Transaction


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "currency",
            "status",
            "description",
            "created_at",
        ]


class TransactionHistoryView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        queryset = Transaction.objects.filter(
            user_id=self.request.user.id
        ).order_by("-created_at", "-id")

        # Filter by start date: ?start_date=2026-10-01
        start_date = self.request.query_params.get("start_date")
        if start_date:
            parsed_start = parse_date(start_date)
            if not parsed_start:
                from rest_framework.exceptions import ValidationError
                raise ValidationError(
                    {"start_date": "Use YYYY-MM-DD format."}
                )
            queryset = queryset.filter(created_at__date__gte=parsed_start)

        # Filter by end date: ?end_date=2026-10-31
        end_date = self.request.query_params.get("end_date")
        if end_date:
            parsed_end = parse_date(end_date)
            if not parsed_end:
                from rest_framework.exceptions import ValidationError
                raise ValidationError(
                    {"end_date": "Use YYYY-MM-DD format."}
                )
            queryset = queryset.filter(created_at__date__lte=parsed_end)

        # Filter by amount: ?min_amount=100&max_amount=500
        min_amount = self.request.query_params.get("min_amount")
        max_amount = self.request.query_params.get("max_amount")

        if min_amount:
            try:
                queryset = queryset.filter(amount__gte=min_amount)
            except (ValueError, TypeError):
                from rest_framework.exceptions import ValidationError
                raise ValidationError(
                    {"min_amount": "Enter a valid amount."}
                )

        if max_amount:
            try:
                queryset = queryset.filter(amount__lte=max_amount)
            except (ValueError, TypeError):
                from rest_framework.exceptions import ValidationError
                raise ValidationError(
                    {"max_amount": "Enter a valid amount."}
                )

        # Filter by status: ?status=SUCCESS
        status = self.request.query_params.get("status")
        if status:
            status = status.upper()
            if status not in ["PENDING", "SUCCESS", "FAILED"]:
                from rest_framework.exceptions import ValidationError
                raise ValidationError(
                    {"status": "Use PENDING, SUCCESS, or FAILED."}
                )
            queryset = queryset.filter(status__iexact=status)

        return queryset