from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserRegistrationSerializer


# Create your views here.
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
