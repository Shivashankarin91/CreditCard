from django.urls import path
from . import views

urlpatterns = [
    path(
        "history/",
        views.transaction_history,
        name="transaction_history",
    ),
    path(
        "daily-summary/",
        views.daily_payment_summary,
        name="daily_payment_summary",
    ),
]

