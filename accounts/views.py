from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .models import User
from .serializers import UserRegistrationSerializer


# Create your views here.
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class CustomAuthToken(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "detail": "Make a POST request with 'username' (telegram_username) and 'password' to obtain a token.",
            },
            status=status.HTTP_200_OK,
        )
