from datetime import date
from decimal import Decimal, InvalidOperation
from django.db.models import Count, Sum, Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.functions import TruncDate
from .models import Transaction


@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(
        user=request.user
    )

    start_date = request.GET.get("start_date", "").strip()
    end_date = request.GET.get("end_date", "").strip()
    min_amount = request.GET.get("min_amount", "").strip()
    max_amount = request.GET.get("max_amount", "").strip()
    status = request.GET.get("status", "").strip()

    errors = []

    # Filter by starting date
    if start_date:
        try:
            parsed_start = date.fromisoformat(start_date)
            transactions = transactions.filter(
                created_at__date__gte=parsed_start
            )
        except ValueError:
            errors.append("Enter a valid start date.")

    # Filter by ending date
    if end_date:
        try:
            parsed_end = date.fromisoformat(end_date)
            transactions = transactions.filter(
                created_at__date__lte=parsed_end
            )
        except ValueError:
            errors.append("Enter a valid end date.")

    # Filter by minimum amount
    if min_amount:
        try:
            amount = Decimal(min_amount)
            if not amount.is_finite() or amount < 0:
                raise ValueError
            transactions = transactions.filter(
                amount__gte=amount
            )
        except (InvalidOperation, ValueError):
            errors.append("Enter a valid minimum amount.")

    # Filter by maximum amount
    if max_amount:
        try:
            amount = Decimal(max_amount)
            if not amount.is_finite() or amount < 0:
                raise ValueError
            transactions = transactions.filter(
                amount__lte=amount
            )
        except (InvalidOperation, ValueError):
            errors.append("Enter a valid maximum amount.")

    # Filter by transaction status
    valid_statuses = {
        choice[0] for choice in Transaction.STATUS_CHOICES
    }

    if status:
        if status in valid_statuses:
            transactions = transactions.filter(status=status)
        else:
            errors.append("Select a valid transaction status.")

    if start_date and end_date:
        try:
            if date.fromisoformat(start_date) > date.fromisoformat(end_date):
                errors.append("Start date must not be after end date.")
        except ValueError:
            pass

    if min_amount and max_amount:
        try:
            low = Decimal(min_amount)
            high = Decimal(max_amount)
            if low.is_finite() and high.is_finite() and low > high:
                errors.append("Minimum amount must not exceed maximum.")
        except InvalidOperation:
            pass

    if errors:
        transactions = Transaction.objects.none()

    context = {
        "transactions": transactions,
        "errors": errors,
        "start_date": start_date,
        "end_date": end_date,
        "min_amount": min_amount,
        "max_amount": max_amount,
        "selected_status": status,
        "status_choices": Transaction.STATUS_CHOICES,
    }

    return render(
        request,
        "transactions/transaction_history.html",
        context,
    )

@staff_member_required
def daily_payment_summary(request):
    daily_summary = (
        Transaction.objects
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(
            total_transactions=Count("id"),

            successful_count=Count(
                "id", filter=Q(status="SUCCESS")
            ),
            successful_amount=Sum(
                "amount", filter=Q(status="SUCCESS")
            ),

            pending_count=Count(
                "id", filter=Q(status="PENDING")
            ),
            failed_count=Count(
                "id", filter=Q(status="FAILED")
            ),
        )
        .order_by("-day")
    )

    return render(
        request,
        "transactions/daily_payment_summary.html",
        {"daily_summary": daily_summary},
    )