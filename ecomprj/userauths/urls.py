from django.urls import path
from . import views

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.register_user, name="sign-up"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
