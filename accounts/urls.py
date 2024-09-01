from django.urls import path

from . import views

urlpatterns = [
    path("profile", views.profile, name="profile"),
    path("sign-in/", views.sign_in, name="sign_in"),
    path("sign-out/", views.sign_out, name="sign_out"),
    path("sign-up/", views.sign_up, name="sign_up"),
    # path('rate-course/<int:course_id>/', views.rate_course, name='rate_course'),
]
