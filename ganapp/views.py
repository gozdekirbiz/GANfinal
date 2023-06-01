from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django import forms
from django.core.files.base import ContentFile

from ganapp.models import UserImage
import os
import matplotlib.pyplot as plt
import numpy as np

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from ganapp.signup import signup
from ganapp.home import home_view

from django.contrib.auth.decorators import login_required

from allauth.account.views import LoginView
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Retrieve username and password from the form
        username = form.cleaned_data.get("login")
        password = form.cleaned_data.get("password")

        # Authenticate the user
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)

            if user.is_superuser:
                return redirect("admin:index")
            else:
                return redirect(self.get_success_url())  # Add parentheses here
        else:
            # Handle invalid credentials
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("home")  # Replace 'home' with the desired URL for regular users


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def archive_view(request):
    # Retrieve all the generated images for the current user
    user_images = UserImage.objects.filter(user=request.user)
    return render(request, "archive.html", {"user_images": user_images})


def delete_image(request, image_id):
    if request.method == "POST":
        image = get_object_or_404(UserImage, id=image_id)
        image.delete()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect

User = get_user_model()


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse(
                {"success": True, "message": "Your password was successfully updated!"}
            )
        else:
            print(form.errors)
            return JsonResponse(
                {"success": False, "message": "Please correct the error below."},
                status=400,
            )
    else:
        return JsonResponse(
            {"success": False, "message": "Invalid request"}, status=400
        )
    print(request.POST)


@login_required
def delete_account(request):
    if request.method == "POST":
        password = request.POST.get("confirm_password")
        user = request.user
        if user.check_password(password):
            user.delete()
            logout(request)
            return JsonResponse(
                {"success": True, "message": "Account deleted successfully."},
                status=200,
            )
        else:
            return JsonResponse(
                {"success": False, "message": "Incorrect password. Please try again."},
                status=400,
            )


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Suggestion


@csrf_exempt
@login_required
def send_suggestion(request):
    if request.method == "POST":
        suggestion_text = request.POST.get("suggestion")
        if suggestion_text:
            suggestion = Suggestion(user=request.user, text=suggestion_text)
            suggestion.save()
            return JsonResponse(
                {"success": True, "message": "Suggestion sent successfully."},
                status=200,
            )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Suggestion field cannot be empty. Please try again.",
                },
                status=400,
            )


def settings(request):
    return render(request, "settings.html")
