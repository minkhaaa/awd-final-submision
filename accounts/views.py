# Create your views here.
from django.http import HttpRequest
from django.shortcuts import render


def profile(request: HttpRequest):
    return render(request, "accounts/profile.html")


# Create your views here.
