# Create your views here.
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course, Enrollment

from .forms import CustomUserCreationForm
from .models import StatusUpdate

User = get_user_model()


@login_required
def profile_view(request, username):
    # Get the user object for the given username
    user = get_object_or_404(User, username=username)

    # Fetch the status updates for this user
    updates = StatusUpdate.objects.filter(user=user).order_by("-updated_at")
    paginator = Paginator(updates, 10)  # Display 10 updates per page
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Fetch the courses this user is enrolled in
    registered_course_ids = Enrollment.objects.filter(user=user).values_list(
        "course_id", flat=True
    )
    registered_courses = Course.objects.filter(id__in=registered_course_ids)

    return render(
        request,
        "accounts/profile_page.html",
        {
            "profile_user": user,
            "page_obj": page_obj,
            "registered_courses": registered_courses,
        },
    )


def check_field(request, field_name):
    form = CustomUserCreationForm(request.GET)

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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sign_in")
    else:
        form = CustomUserCreationForm()
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


# Create your views here.
