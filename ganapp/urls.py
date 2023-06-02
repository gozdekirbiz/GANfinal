from . import views
from . import signup
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from . import home
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path(
        "accounts/login/",
        views.CustomLoginView.as_view(template_name="account/login.html"),
        name="account_login",
    ),
    path(
        "accounts/password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/registration/password_reset_form.html"
        ),
        name="account_password_reset",
    ),
    path(
        "accounts/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/registration/password_reset_done.html"
        ),
        name="account_password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/registration/password_reset_confirm.html"
        ),
        name="account_password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/registration/password_reset_complete.html"
        ),
        name="account_password_reset_complete",
    ),
    path("accounts/", include("allauth.urls")),
    path("home/", views.home_view, name="home"),
    path("archive/", views.archive_view, name="archive"),
    path("delete_image/<int:image_id>/", views.delete_image, name="delete_image"),
    path("activate/<str:uidb64>/<str:token>/", signup.activate, name="activate"),
    path("result/", home.result_view, name="result"),
    path("settings/", views.settings, name="settings"),
    path("change_password/", views.change_password, name="change_password"),
    path("delete_account/", views.delete_account, name="delete_account"),
    path("send_suggestion/", views.send_suggestion, name="send_suggestion"),
    path("kvkk/", views.kvkk, name="kvkk"),
    path("logout/", views.logout_view, name="account_logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
