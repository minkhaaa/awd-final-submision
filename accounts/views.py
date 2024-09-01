# Create your views here.
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignUpForm


def check_field(request, field_name):
    form = SignUpForm(request.GET)

    if form.is_valid():
        return render(
            request, "accounts/error_messages.html", {"messages": []}
        )  # No errors, return an empty response
    else:
        error_message = form.errors.get(field_name)
        if error_message:
            return render(
                request, "accounts/error_messages.html", {"messages": error_message}
            )
        else:
            return HttpResponse("<div class='errors'> </div>")


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
