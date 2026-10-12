import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "currency",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "currency",
        "created_at",
    )

    search_fields = ("user__username",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"

    search_fields = (
        "user__username",
        "description",
    )

    actions = ["export_transactions_csv"]

    @admin.action(description="Export selected transactions to CSV")
    def export_transactions_csv(self, request, queryset):
        # Require Django Admin superuser privileges for export.
        if not request.user.is_superuser:
            self.message_user(
                request,
                "Only superusers can export transactions.",
                level="ERROR",
            )
            return None

        response = HttpResponse(
            content_type="text/csv; charset=utf-8"
        )
        response["Content-Disposition"] = (
            'attachment; filename="transactions.csv"'
        )

        # Helps spreadsheet applications recognize UTF-8.
        response.write("\ufeff")

        writer = csv.writer(response)
        writer.writerow([
            "Transaction ID",
            "Username",
            "Amount",
            "Currency",
            "Status",
            "Description",
            "Created At",
        ])

        for transaction in queryset.select_related("user").iterator():
            writer.writerow([
                transaction.id,
                transaction.user.get_username(),
                transaction.amount,
                transaction.currency,
                transaction.status,
                transaction.description,
                transaction.created_at.isoformat(),
            ])

        return response

