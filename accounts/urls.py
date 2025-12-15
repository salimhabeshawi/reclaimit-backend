from django.urls import path

from .views import CustomAuthToken, RegistrationView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", CustomAuthToken.as_view(), name="login"),
]
