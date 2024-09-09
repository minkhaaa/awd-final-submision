# Create your views here.
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from courses.models import Course, Enrollment

from .forms import CustomUserCreationForm
from .models import Block, StatusUpdate

User = get_user_model()


@login_required
def profile_view(request, username):
    # Get the user object for the given username
    profile_user = get_object_or_404(User, username=username)

    # Check if the logged-in user has blocked the profile user
    has_blocked = Block.objects.filter(
        blocker=request.user, blocked=profile_user
    ).exists()

    # Check if the profile user has blocked the logged-in user
    is_blocked_by = Block.objects.filter(
        blocker=profile_user, blocked=request.user
    ).exists()

    # If either user is blocked, return a forbidden response
    if is_blocked_by:
        return HttpResponseForbidden("This user has blocked you.")

    # Fetch the status updates for this user
    updates = StatusUpdate.objects.filter(user=profile_user).order_by("-updated_at")
    paginator = Paginator(updates, 10)  # Display 10 updates per page
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Fetch the courses this user is enrolled in
    registered_course_ids = Enrollment.objects.filter(user=profile_user).values_list(
        "course_id", flat=True
    )
    registered_courses = Course.objects.filter(id__in=registered_course_ids)

    # Pass block status to the template
    return render(
        request,
        "accounts/profile_page.html",
        {
            "profile_user": profile_user,
            "page_obj": page_obj,
            "registered_courses": registered_courses,
            "has_blocked": has_blocked,  # Whether the logged-in user has blocked the profile user
        },
    )


# Functionality to block a user
@login_required
def block_user(request, username):
    user_to_block = get_object_or_404(User, username=username)

    if user_to_block == request.user:
        return HttpResponseForbidden("You cannot block yourself.")

    # Check if the block already exists
    if not Block.objects.filter(blocker=request.user, blocked=user_to_block).exists():
        Block.objects.create(blocker=request.user, blocked=user_to_block)
        messages.success(request, f"You have blocked {user_to_block.username}.")
    return HttpResponseRedirect(reverse("profile_view", args=[username]))


# Functionality to unblock a user
@login_required
def unblock_user(request, username):
    user_to_unblock = get_object_or_404(User, username=username)

    block = Block.objects.filter(blocker=request.user, blocked=user_to_unblock).first()

    if block:
        block.delete()
        messages.success(request, f"You have unblocked {user_to_unblock.username}.")
    return HttpResponseRedirect(reverse("profile_view", args=[username]))


# Functionality for teachers to remove a user
@login_required
def remove_user(request, username):
    user_to_remove = get_object_or_404(User, username=username)

    if not request.user.is_teacher:
        return HttpResponseForbidden("Only teachers can remove users.")

    # Make sure a teacher cannot remove themselves
    if user_to_remove == request.user:
        return HttpResponseForbidden("You cannot remove yourself.")

    user_to_remove.delete()
    messages.success(
        request, f"User {user_to_remove.username} has been removed from the system."
    )
    return HttpResponseRedirect(reverse("main_page"))


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
