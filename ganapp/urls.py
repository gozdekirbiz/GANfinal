from . import views
from . import signup
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from ganapp.home import result_view

urlpatterns = [
    path(
        "accounts/login/",
        views.CustomLoginView.as_view(template_name="account/login.html"),
        name="account_login",
    ),
    path("accounts/", include("allauth.urls")),
    path("home/", views.home_view, name="home"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("archive/", views.archive_view, name="archive"),
    path("delete_image/<int:image_id>/", views.delete_image, name="delete_image"),
    path("activate/<str:uidb64>/<str:token>/", signup.activate, name="activate"),
    path("result/", result_view, name="result"),
    path("settings/", views.settings, name="settings"),
    path("change_password/", views.change_password, name="change_password"),
    path("delete_account/", views.delete_account, name="delete_account"),
    path("send_suggestion/", views.send_suggestion, name="send_suggestion"),
]
