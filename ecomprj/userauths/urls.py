from django.urls import path
from . import views

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.register_user, name="sign-up"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/update/", views.profile_update, name="profile-update"),
    path("change-password/", views.change_password, name="change-password"),
    path("verify-email/", views.email_verification_request, name="verify-email"),
    path("email/activate/<uidb64>/<token>/", views.email_verifier, name="email-activate"),
]
