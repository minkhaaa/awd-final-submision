from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.models import StatusUpdate, User
from courses.models import Course, Enrollment, Rating, Topic

from .serializers import (
    CourseSerializer,
    EnrollmentSerializer,
    RatingSerializer,
    StatusUpdateSerializer,
    TopicSerializer,
    UserSerializer,
)


# User ViewSet (Allow POST to create users)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated users to create accounts


# StatusUpdate ViewSet (Disallow POST requests)
class StatusUpdateViewSet(viewsets.ModelViewSet):
    queryset = StatusUpdate.objects.all()
    serializer_class = StatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Creating status updates via API is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


# Course ViewSet (Disallow POST requests)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Creating courses via API is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


# Topic ViewSet (Disallow POST requests)
class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Creating topics via API is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


# Enrollment ViewSet (Disallow POST requests)
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Creating enrollments via API is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


# Rating ViewSet (Disallow POST requests)
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "Creating ratings via API is not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
