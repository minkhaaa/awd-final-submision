from django.urls import path

from . import views

urlpatterns = [
    path("profile", views.profile, name="profile"),
    # path('rate-course/<int:course_id>/', views.rate_course, name='rate_course'),
]
