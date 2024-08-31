from django.test import TestCase
from django.urls import reverse

from accounts.models import Teacher, User

from .models import Course, Topic


class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="robert", password="testpassword", is_teacher=True
        )
        self.teacher = Teacher.objects.create(user=self.user)
        self.course = Course.objects.create(
            title="Discrete Maths",
            description="Build your foundation with this 5 weeks course.",
            instructor=self.teacher,
        )
        self.topic = Topic.objects.create(
            course=self.course,
            title="Introduction to Discrete Maths",
            body="This is the first topic of the course.",
        )

    def test_course_creation(self):
        self.assertEqual(self.course.title, "Discrete Maths")
        self.assertEqual(
            self.course.description, "Build your foundation with this 5 weeks course."
        )
        self.assertEqual(self.course.instructor.user.username, "robert")

    def test_topic_creation(self):
        self.assertEqual(self.topic.title, "Introduction to Discrete Maths")
        self.assertEqual(self.topic.body, "This is the first topic of the course.")
        self.assertEqual(self.topic.course.title, "Discrete Maths")


class CourseViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="robert", password="testpassword", is_teacher=True
        )
        self.teacher = Teacher.objects.create(user=self.user)
        self.course = Course.objects.create(
            title="Discrete Maths",
            description="Build your foundation with this 5 weeks course.",
            instructor=self.teacher,
        )

    def test_main_page_view(self):
        response = self.client.get(reverse("main_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "courses/main_page.html")

    def test_course_detail_view(self):
        response = self.client.get(reverse("course_detail", args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "courses/course_detail.html")
