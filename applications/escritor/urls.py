# Django
from django.urls import path

# Views
from . import views
app_name = "users_app"

urlpatterns = [
    #Template login
    path(
        'register/',
        views.RegisterNewUserAPIView.as_view(),
        name = "register-user",
    ),
    path(
        'login/',
        views.LoginUserAPIView.as_view(),
        name = "login-user",
    )
]