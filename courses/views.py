import os

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render

from .models import Course, Topic


def main_page(request):
    courses = Course.objects.all()
    return render(request, "courses/main_page.html", {"courses": courses})


from .models import Course, Topic


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
