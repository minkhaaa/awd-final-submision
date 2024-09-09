from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts.models import StatusUpdate
from courses.models import Enrollment, Rating

from .factories import CourseFactory, StudentFactory, TeacherFactory


class APITestBase(APITestCase):
    def setUp(self):
        # Use factories to create test data
        self.teacher = TeacherFactory()
        self.student = StudentFactory()
        self.course = CourseFactory(instructor=self.teacher)
        # Set up APIClient
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher.user)


class UserViewSetTests(APITestBase):
    def test_create_user(self):
        """Test creating a new user"""
        response = self.client.post(
            reverse("user-list"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "testpass",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CourseViewSetTests(APITestBase):
    def test_create_course_forbidden(self):
        """Test that creating a new course via the API is forbidden"""
        response = self.client.post(
            reverse("course-list"),
            {
                "title": "New Course",
                "description": "New Description",
                "instructor": self.teacher.user.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class EnrollmentViewSetTests(APITestBase):
    def test_create_enrollment_forbidden(self):
        """Test that creating an enrollment via the API is forbidden"""
        response = self.client.post(
            reverse("enrollment-list"),
            {"user": self.student.user.id, "course": self.course.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class RatingViewSetTests(APITestBase):
    def test_create_rating_forbidden(self):
        """Test that creating a rating via the API is forbidden"""
        response = self.client.post(
            reverse("rating-list"),
            {
                "user": self.student.user.id,
                "course": self.course.id,
                "rating": 4,
                "comment": "Good!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
