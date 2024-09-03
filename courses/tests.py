from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Student, Teacher

from .models import Course, Enrollment

User = get_user_model()


class AllCoursesViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.teacher = Teacher.objects.create(user=self.user)
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", instructor=self.teacher
        )

    def test_all_courses_view_for_guest_user(self):
        response = self.client.get(reverse("all_courses"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Course")

    def test_all_courses_view_for_authenticated_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("all_courses"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Course")


class MyCoursesViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a user and then associate with a Teacher instance
        self.teacher_user = User.objects.create_user(
            username="teacher", password="testpass", email="teacher@example.com"
        )
        self.teacher_user.is_teacher = True
        self.teacher_user.save()
        self.teacher = Teacher.objects.create(user=self.teacher_user)

        # Create a user and then associate with a Student instance
        self.student_user = User.objects.create_user(
            username="student", password="testpass", email="student@example.com"
        )
        self.student_user.is_student = True
        self.student_user.save()
        self.student = Student.objects.create(user=self.student_user)

        # Create a course assigned to the teacher
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", instructor=self.teacher
        )

        # Enroll the student in the course
        Enrollment.objects.create(user=self.student_user, course=self.course)

    def test_my_courses_view_for_teacher(self):
        self.client.login(username="teacher", password="testpass")
        response = self.client.get(reverse("my_courses"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Course")

    def test_my_courses_view_for_student(self):
        self.client.login(username="student", password="testpass")
        response = self.client.get(reverse("my_courses"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Course")

    def test_my_courses_view_for_guest(self):
        response = self.client.get(reverse("my_courses"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Course")


class EnrollInCourseTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a user and then associate with a Teacher instance
        self.teacher_user = User.objects.create_user(
            username="teacher", password="testpass", email="teacher@example.com"
        )
        self.teacher_user.is_teacher = True
        self.teacher_user.save()
        self.teacher = Teacher.objects.create(user=self.teacher_user)

        # Create a user and then associate with a Student instance
        self.student_user = User.objects.create_user(
            username="student", password="testpass", email="student@example.com"
        )
        self.student_user.is_student = True
        self.student_user.save()
        self.student = Student.objects.create(user=self.student_user)

        # Create a course assigned to the teacher
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", instructor=self.teacher
        )
        # Enroll the student in the course
        Enrollment.objects.create(user=self.student_user, course=self.course)

    def test_enroll_in_course_as_student(self):
        self.client.login(username="student", password="testpass")
        response = self.client.post(reverse("enroll_in_course", args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Enrollment.objects.filter(
                user=self.student_user, course=self.course
            ).exists()
        )

    def test_enroll_in_course_as_guest(self):
        response = self.client.post(reverse("enroll_in_course", args=[self.course.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertRedirects(
            response, f"/accounts/login/?next=/enroll/{self.course.id}/"
        )


class ViewEnrollmentsTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a user and then associate with a Teacher instance
        self.teacher_user = User.objects.create_user(
            username="teacher", password="testpass", email="teacher@example.com"
        )
        self.teacher_user.is_teacher = True
        self.teacher_user.save()
        self.teacher = Teacher.objects.create(user=self.teacher_user)

        # Create a user and then associate with a Student instance
        self.student_user = User.objects.create_user(
            username="student", password="testpass", email="student@example.com"
        )
        self.student_user.is_student = True
        self.student_user.save()
        self.student = Student.objects.create(user=self.student_user)

        # Create a course assigned to the teacher
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", instructor=self.teacher
        )

        # Enroll the student in the course
        Enrollment.objects.create(user=self.student_user, course=self.course)

    def test_view_enrollments_as_teacher(self):
        self.client.login(username="teacher", password="testpass")
        response = self.client.get(reverse("view_enrollments", args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "student")

    def test_view_enrollments_as_student(self):
        self.client.login(username="student", password="testpass")
        response = self.client.get(reverse("view_enrollments", args=[self.course.id]))
        self.assertEqual(response.status_code, 403)  # Students should not access this


class CreateCourseViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.teacher_user = User.objects.create_user(
            username="teacher", password="testpass", email="email@gmail.com"
        )
        self.teacher = Teacher.objects.create(user=self.teacher_user)

    def test_create_course_view_for_non_teacher(self):
        non_teacher_user = User.objects.create_user(
            username="nonteacher", password="testpass"
        )
        self.client.login(username="nonteacher", password="testpass")
        response = self.client.get(reverse("create_course"))
        self.assertRedirects(response, reverse("main_page"))
