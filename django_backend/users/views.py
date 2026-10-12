from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Card
from .serializers import CardSerializer
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):

    def post(self, request):

        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response(
                {
                    "error": "Username, email and password are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {
                    "error": "Username already exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response(
            {
                "message": "User registered successfully",
                "username": user.username,
                "email": user.email
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Logout
class LogoutView(APIView):
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"msg": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

# Protected Route Example
class ProtectedView(APIView):
    
    def get(self, request):
        return Response({"msg": f"Hello {request.user.username}, you accessed a protected route!"})    

class AddCardView(APIView):
    serializer_class = CardSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# View Saved Cards
class ListCardsView(APIView):
    serializer_class = CardSerializer
    

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

# Delete Card
class DeleteCardView(APIView):
    serializer_class = CardSerializer
    
    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "JWT authentication successful!",
            "username": request.user.username,
            "email": request.user.email
        })