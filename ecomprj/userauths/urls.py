from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "userauths"

urlpatterns = [
    path("sign-up/", views.register_user, name="sign-up"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/update/", views.profile_update, name="profile-update"),
    path("change-password/", views.change_password, name="change-password"),
    path("verify-email/", views.email_verification_request, name="verify-email"),
    path("email/activate/<uidb64>/<token>/", views.email_verifier, name="email-activate"),
    path('admin/password_reset/',auth_views.PasswordResetView.as_view(),name='admin_password_reset'),
    path('admin/password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]
