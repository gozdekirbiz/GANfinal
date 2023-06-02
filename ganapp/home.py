from django.contrib.auth.decorators import login_required
from django import forms
from ganapp.generator import Cartoonize
from ganapp.cycleGANGen import CycleGANGenerator
from ganapp.models import UserImage
import time
from django.http import JsonResponse
from django.shortcuts import render
import tempfile
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class ImageUploadForm(forms.Form):
    selectOption = forms.ChoiceField(
        choices=[
            ("cartoon", "CartoonGan"),
            ("monet", "CycleGan - Monet"),
            ("vangogh", "CycleGan - Vangogh"),
            ("cezanne", "CycleGan - Cezanne"),
            ("ukiyoe", "CycleGan - Ukiyoe"),
        ],
        widget=forms.Select(attrs={"class": "style-select"}),
        required=True,
    )

    image = forms.ImageField(label="Upload Image")
    # Diğer alanlar


def getModel(style):
    if style == "cartoon":
        return Cartoonize()
    else:
        return CycleGANGenerator(style)


from django.http import JsonResponse


@login_required
def home_view(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            style = form.cleaned_data["selectOption"]
            cartoonizer = getModel(style)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
                temp.write(request.FILES["image"].read())
                cartoon_image = cartoonizer.forward(temp.name)
                # Save the original image and the cartoonized image to the database
                user_image = UserImage(
                    user=request.user,
                    image=request.FILES["image"],
                    output_image=cartoon_image,
                    style=style,
                )
                user_image.save()
                # Add delay to simulate AI processing time
                time.sleep(5)  # Adjust the delay duration as needed
                return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors.as_json()})
    else:
        form = ImageUploadForm()
        user_images = UserImage.objects.filter(user=request.user).last()
        return render(request, "home.html", {"form": form, "user_images": user_images})


@login_required
def result_view(request):
    user_images = UserImage.objects.filter(user=request.user).last()
    return render(request, "result.html", {"user_images": user_images})
