from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.news_feed_view, name="main_page"),
    path("course/<int:course_id>/", views.course_detail, name="course_detail"),
    path("course/<int:course_id>/add-topic/", views.add_topic, name="add_topic"),
    path(
        "download/<int:topic_id>/",
        views.download_attachment,
        name="download_attachment",
    ),
    path("rate-course/<int:course_id>/", views.main_page, name="rate_course"),
    path("enroll/<int:course_id>/", views.enroll_in_course, name="enroll_in_course"),
    path("all-courses/", views.all_courses_view, name="all_courses"),
    path("my-courses/", views.my_courses_view, name="my_courses"),
    path(
        "courses/<int:course_id>/reviews/",
        views.course_reviews_view,
        name="course_reviews",
    ),
    path(
        "courses/<int:course_id>/feedback/",
        views.show_feedback_form_view,
        name="show_feedback_form",
    ),
    path(
        "courses/<int:course_id>/submit_feedback/",
        views.submit_feedback_view,
        name="submit_feedback",
    ),
    path(
        "courses/<int:course_id>/enrollments/",
        views.view_enrollments,
        name="view_enrollments",
    ),
    path("courses/create/", views.create_course_view, name="create_course"),
    path("news-feed/", views.news_feed_view, name="news_feed"),
    path("search/", views.news_feed_view, name="user_list"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
