import os

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from accounts.models import Student

from .models import Course, Enrollment, Topic


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
        "courses/tabs_with_courses.html",
        {
            "courses": courses,
            "active_tab": "all_courses",
            "enrolled_course_ids": enrolled_course_ids,
        },
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
        "courses/tabs_with_courses.html",
        {"courses": courses, "active_tab": "my_courses"},
    )


@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        Enrollment.objects.create(user=request.user, course=course)

        # Check if the user is not already a student and create a Student object
        if not request.user.is_student:
            request.user.is_student = True
            request.user.save()
            Student.objects.create(user=request.user)
    # Return a partial update to replace the "Enroll" button with "Enrolled"
    return HttpResponse('<span class="text-green-500 font-bold">Enrolled</span>')


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
    return render(
        request,
        "courses/_course_detail.html",
        {"course": course, "topics": topics},
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
