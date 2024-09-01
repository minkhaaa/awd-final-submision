# Create your views here.
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .forms import SignUpForm


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "sign_in"
            )  # Redirect to the sign-in page after successful registration
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, "accounts/sign_up.html", {"form": form})


def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(
                "main_page"
            )  # Redirect to the main page or another page as needed
    else:
        form = AuthenticationForm()
    return render(request, "accounts/sign_in.html", {"form": form})


def sign_out(request):
    logout(request)
    return render(
        request, "accounts/sign_out.html"
    )  # Redirect to the home page or another page as needed


def profile(request: HttpRequest):
    return render(request, "accounts/profile.html")


# Create your views here.
