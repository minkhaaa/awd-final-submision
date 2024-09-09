import os
from logging import log
from re import search

from django.contrib.auth.decorators import PermissionDenied, login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from accounts.forms import StatusUpdateForm
from accounts.models import Block, StatusUpdate, Student, Teacher, User

from .forms import RatingForm  # Assuming you have a form for submitting ratings
from .forms import CourseForm
from .models import Course, Enrollment, Rating, Topic


def news_feed_view(request):
    # Handle the status update form submission
    if request.method == "POST":
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            status_update = form.save(commit=False)
            status_update.user = request.user
            status_update.save()
            if "HX-Request" in request.headers:
                return render(
                    request,
                    "accounts/_status_update_single.html",
                    {"update": status_update},
                )
            return redirect("main_page")
    else:
        form = StatusUpdateForm()

    # Determine blocked and blocking users
    if request.user.is_authenticated:
        # Get IDs of users who have blocked the current user
        blocked_by_user_ids = Block.objects.filter(blocked=request.user).values_list(
            "blocker_id", flat=True
        )

        # Get IDs of users whom the current user has blocked
        blocking_user_ids = Block.objects.filter(blocker=request.user).values_list(
            "blocked_id", flat=True
        )

        # Combine both sets of user IDs
        blocked_user_ids = set(blocked_by_user_ids) | set(blocking_user_ids)
    else:
        blocked_user_ids = []

    # Fetch all status updates for the news feed, excluding updates from blocked users
    updates = StatusUpdate.objects.exclude(user__id__in=blocked_user_ids).order_by(
        "-updated_at"
    )
    paginator = Paginator(updates, 10)  # Display 10 updates per page
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Fetch all courses to be passed to the '_tabs_with_courses.html'
    courses = Course.objects.all()
    enrolled_course_ids = []
    search_query = request.GET.get("search", "")

    # Base QuerySet for filtering users
    if request.user.is_authenticated and request.user.is_teacher:
        # Teachers can view and search all users
        users = User.objects.exclude(id__in=blocked_user_ids)
    else:
        # Students and guests can only view and search students, excluding blocked ones
        users = User.objects.filter(is_student=True).exclude(id__in=blocked_user_ids)

    # Apply search query if provided
    if search_query:
        users = users.filter(username__icontains=search_query)

    # If the user is authenticated, get their enrolled course IDs
    if request.user.is_authenticated:
        enrolled_course_ids = list(
            Enrollment.objects.filter(user=request.user).values_list(
                "course_id", flat=True
            )
        )

    # Check if the request is an HTMX request for infinite scroll
    if "HX-Request" in request.headers and "page" in request.GET:
        return render(
            request,
            "courses/_pagination_handler.html",
            {"page_obj": page_obj, "page_number": page_number},
        )

    # Pass all necessary context to the main page template
    return render(
        request,
        "courses/main_page.html",
        {
            "form": form,  # Pass the status update form
            "page_obj": page_obj,  # Pass the paginated status updates
            "courses": courses,  # Pass the courses
            "enrolled_course_ids": enrolled_course_ids,  # Pass the enrolled course IDs
            "page_number": page_number,
            "users": users,  # Pass the filtered user list
        },
    )


@login_required
def create_course_view(request):
    if not request.user.is_teacher:
        return redirect("main_page")  # Redirect non-teachers to the main page

    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = (
                request.user.teacher
            )  # Set the instructor to the logged-in teacher
            course.save()
            return redirect(
                "main_page"
            )  # Redirect to the course detail page after creation
    else:
        form = CourseForm()

    return render(request, "courses/create_course.html", {"form": form})


def all_courses_view(request):
    courses = Course.objects.all()
    enrolled_course_ids = []

    if request.user.is_authenticated:
        enrolled_course_ids = list(
            Enrollment.objects.filter(user=request.user).values_list(
                "course_id", flat=True
            )
        )
    return render(
        request,
        "courses/_tabs_with_courses.html",
        {
            "courses": courses,
            "active_tab": "all_courses",
            "enrolled_course_ids": enrolled_course_ids,
        },
    )


@login_required
def view_enrollments(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Only the instructor of the course should be able to view enrollments
    if not request.user.is_teacher or request.user.teacher != course.instructor:
        return HttpResponseForbidden("You do not have permission to view this page.")

    # Fetch all students enrolled in this course
    enrollments = Enrollment.objects.filter(course=course).select_related("user")

    return render(
        request,
        "courses/_enrollment_list.html",
        {"enrollments": enrollments, "course": course},
    )


def my_courses_view(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            courses = Course.objects.filter(instructor=request.user.teacher)
        else:
            courses = Course.objects.filter(enrollments__user=request.user)
    else:
        courses = Course.objects.none()
    return render(
        request,
        "courses/_tabs_with_courses.html",
        {"courses": courses, "active_tab": "my_courses"},
    )


@login_required
def show_feedback_form_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Ensure the user is enrolled before showing the form
    if not request.user.enrollments.filter(course=course).exists():
        return HttpResponseForbidden("You are not enrolled in this course.")

    form = RatingForm()  # Instantiate an empty form
    return render(
        request, "courses/_feedback_form.html", {"form": form, "course": course}
    )


@login_required
def submit_feedback_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Ensure the user is enrolled before allowing submission
    if not request.user.enrollments.filter(course=course).exists():
        return HttpResponseForbidden("You are not enrolled in this course.")

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.course = course
            rating.save()
            return HttpResponse(
                '<p class="text-green-500">Thank you for your feedback!</p>'
            )

    # If form is not valid, re-render the form with errors
    form = RatingForm()
    return render(
        request, "courses/_feedback_form.html", {"form": form, "course": course}
    )


@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    topics = course.topics.all()
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        Enrollment.objects.create(user=request.user, course=course)

        # Check if the user is not already a student and create a Student object
        if not request.user.is_student:
            request.user.is_student = True
            request.user.save()
            Student.objects.create(user=request.user)

    # Partial update for the button
    response_content = '<span class="text-green-500 font-bold">Enrolled</span>'

    # Add OOB content to update another div
    response_content += render_to_string(
        "courses/_enrolled_topics.html", {"topics": topics}
    )

    return HttpResponse(response_content)


def main_page(request):
    courses = Course.objects.all()
    enrolled_course_ids = []

    if request.user.is_authenticated:
        enrolled_course_ids = list(
            Enrollment.objects.filter(user=request.user).values_list(
                "course_id", flat=True
            )
        )

    return render(
        request,
        "courses/main_page.html",
        {
            "courses": courses,
            "enrolled_course_ids": enrolled_course_ids,
        },
    )


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    topics = course.topics.all()  # Assuming related name 'topics' in Topic model
    # Calculate the average rating for the course
    average_rating = Rating.objects.filter(course=course).aggregate(Avg("rating"))[
        "rating__avg"
    ]

    # Round the average rating to 1 decimal place if not None
    if average_rating is not None:
        average_rating = round(average_rating, 1)
    if request.user.is_authenticated:
        # Check if the user is enrolled in the course
        is_enrolled = Enrollment.objects.filter(
            user=request.user, course=course
        ).exists()
        # Check if the user has already submitted a review for this course
        has_submitted_review = Rating.objects.filter(
            user=request.user, course=course
        ).exists()
    else:
        is_enrolled = has_submitted_review = False
    return render(
        request,
        "courses/_course_detail.html",
        {
            "course": course,
            "topics": topics,
            "average_rating": average_rating,
            "is_enrolled": is_enrolled,
            "has_submitted_review": has_submitted_review,
        },
    )


def course_reviews_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    ratings = (
        Rating.objects.filter(course=course)
        .select_related("user")
        .order_by("-rated_at")
    )

    return render(
        request,
        "courses/_course_reviews.html",
        {
            "course": course,
            "ratings": ratings,
        },
    )


def add_topic(request, course_id):
    if request.method == "POST":
        course = get_object_or_404(Course, id=course_id)
        title = request.POST.get("title")
        body = request.POST.get("body")
        attachment = request.FILES.get("attachment")

        topic = Topic.objects.create(
            course=course, title=title, body=body, attachment=attachment
        )

        # Render the new topic as a partial to be swapped in by HTMX
        return render(request, "courses/_topic.html", {"topic": topic})

    return HttpResponse(status=405)


def download_attachment(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if topic.attachment:
        file_path = topic.attachment.path
        fs = FileSystemStorage()

        if fs.exists(file_path):
            with fs.open(file_path, "rb") as file:
                response = HttpResponse(
                    file.read(), content_type="application/octet-stream"
                )
                response["Content-Disposition"] = (
                    f'attachment; filename="{os.path.basename(file_path)}"'
                )
                return response
        else:
            return HttpResponseNotFound(
                "The requested file was not found on our server."
            )
    else:
        return HttpResponseNotFound("No attachment found for this topic.")
