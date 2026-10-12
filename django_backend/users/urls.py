from django.urls import path
from .views import RegisterView,LoginView,LogoutView,ProtectedView,AddCardView,ListCardsView,DeleteCardView,MyProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("cards/add/", AddCardView.as_view(), name="add-card"),
    path("cards/", ListCardsView.as_view(), name="list-cards"),
    path("cards/<int:pk>/delete/", DeleteCardView.as_view(), name="delete-card"),
    path('me/', MyProfileView.as_view(), name='my-profile'),

]