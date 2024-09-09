from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import (
    CourseViewSet,
    EnrollmentViewSet,
    RatingViewSet,
    StatusUpdateViewSet,
    TopicViewSet,
    UserViewSet,
)
from .views import developer_page

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"status-updates", StatusUpdateViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"topics", TopicViewSet)
router.register(r"enrollments", EnrollmentViewSet)
router.register(r"ratings", RatingViewSet)

# The API URLs are determined automatically by the router
urlpatterns = [
    path("", include(router.urls)),
    path("developer/", developer_page, name="developer_page"),
]
