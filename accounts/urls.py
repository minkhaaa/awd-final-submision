from django.urls import path

from . import views

urlpatterns = [
    path("sign-in/", views.sign_in, name="sign_in"),
    path("accounts/login/", views.sign_in, name="sign_in"),
    path("sign-out/", views.sign_out, name="sign_out"),
    path("sign-up/", views.sign_up, name="sign_up"),
    # path("sign-up/check-email/", views.check_email, name="check_email"),
    path("sign-up/check/<str:field_name>/", views.check_field, name="check_field"),
    # path('rate-course/<int:course_id>/', views.rate_course, name='rate_course'),
    path("profile/<str:username>/", views.profile_view, name="profile_page"),
    path("profile/<str:username>/", views.profile_view, name="profile_view"),
    path("profile/<str:username>/block/", views.block_user, name="block_user"),
    path("profile/<str:username>/unblock/", views.unblock_user, name="unblock_user"),
    path("profile/<str:username>/remove/", views.remove_user, name="remove_user"),
]
