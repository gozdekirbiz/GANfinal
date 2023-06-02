import hmac
import hashlib
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages


def create_token(user):
    msg = str(user.pk) + user.password
    secret = settings.SECRET_KEY.encode()
    token = hmac.new(secret, msg.encode(), hashlib.sha256).digest()
    return token.hex()  # convert bytes to hex string for URL safe


def check_token(user, token):
    expected_token = create_token(user)
    token_bytes = bytes.fromhex(token)  # convert hex string back to bytes
    print("Expected Token:", expected_token)
    print("Received Token:", token_bytes.hex())  # convert bytes to hex for comparison
    result = hmac.compare_digest(expected_token, token_bytes.hex())
    print("Result: ", result)
    return result


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = create_token(user)
            print("Token:", token)
            mail_subject = "Activate your account."
            message = render_to_string(
                "account/email/email_confirmation_signup.html",
                {
                    "user": user,
                    "domain": "localhost:8000",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": token,
                },
            )

            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            print("Email Recipient:", user.email)

            context = {"form": form}
            return render(request, "account/email_confirmation_message.html", context)
        else:
            # Handle errors...
            error_occurred = False
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
                    error_occurred = True
                    break
                if error_occurred:
                    break
            # If there's an error in the form, display the filled form to the user
            context = {"form": form}
    else:
        form = SignUpForm()
        context = {"form": form}

    return render(request, "account/signup.html", context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print("UID:", uid)
        user = get_user_model().objects.get(pk=uid)
        print("User:", user)
        print("Token:", token)
        if check_token(user, token):
            user.is_active = True
            user.save()
            user.backend = "django.contrib.auth.backends.ModelBackend"
            # login(request, user)
            return render(request, "account/activation_success.html")
        else:
            return render(request, "account/activation_invalid.html")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, "account/activation_invalid.html")
