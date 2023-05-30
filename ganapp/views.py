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
