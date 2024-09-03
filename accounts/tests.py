from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from courses.models import Course, Enrollment

from .models import StatusUpdate, Student, Teacher

User = get_user_model()


class ProfileViewTest(TestCase):
    """Tests for the profile_view function"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="minkha", password="29M30a94", email="minkha@example.com"
        )
        self.client.login(username="minkha", password="29M30a94")

    def test_profile_view_status_code(self):
        """Profile view returns a 200 status code for a logged-in user."""
        url = reverse("profile_page", args=[self.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_view_contains_user_info(self):
        """Profile view contains the profile user and registered courses."""
        url = reverse("profile_page", args=[self.user.username])
        response = self.client.get(url)
        self.assertContains(response, self.user.username)

    def test_profile_view_status_updates(self):
        """Profile view displays the status updates of the user."""
        StatusUpdate.objects.create(user=self.user, content="First update")
        StatusUpdate.objects.create(user=self.user, content="Second update")

        url = reverse("profile_page", args=[self.user.username])
        response = self.client.get(url)
        self.assertContains(response, "First update")
        self.assertContains(response, "Second update")

    def test_profile_view_pagination(self):
        """Profile view paginates status updates."""
        for i in range(15):
            StatusUpdate.objects.create(user=self.user, content=f"Update {i}")

        url = reverse("profile_page", args=[self.user.username])
        response = self.client.get(url)
        self.assertEqual(len(response.context["page_obj"]), 10)


class SignUpViewTest(TestCase):
    """Tests for the sign_up function"""

    def test_signup_form_submission(self):
        """Sign up form submission creates a new user and redirects to sign-in page."""
        url = reverse("sign_up")
        response = self.client.post(
            url,
            {
                "first_name": "New",
                "last_name": "user",
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "SecurePass123!",  # Strong password
                "password2": "SecurePass123!",
            },
        )

        # If the response is not a redirect, print form errors for debugging
        if response.status_code != 302:
            form = response.context.get("form")
            if form:
                print("Form Errors:", form.errors)
            else:
                print("No form in context")

        self.assertEqual(
            response.status_code, 302
        )  # Expect a redirect after form submission
        self.assertTrue(User.objects.filter(username="newuser").exists())


class SignInViewTest(TestCase):
    """Tests for the sign_in function"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="minkha", password="29M30a94", email="minkha@example.com"
        )

    def test_signin_page_status_code(self):
        """Sign in page returns a 200 status code."""
        url = reverse("sign_in")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_signin_form_submission(self):
        """Sign in form submission logs in the user and redirects."""
        url = reverse("sign_in")
        response = self.client.post(
            url, {"username": self.user.username, "password": "29M30a94"}
        )
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)


class SignOutViewTest(TestCase):
    """Tests for the sign_out function"""

    def setUp(self):
        self.user = User.objects.create_user(username="minkha", password="29M30a94")
        self.client.login(username="minkha", password="29M30a94")

    def test_signout(self):
        """Sign out logs out the user and redirects to the sign-out page."""
        url = reverse("sign_out")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)


class CheckFieldTest(TestCase):
    """Tests for the check_field function"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="minkha", password="29M30a94", email="minkha@example.com"
        )

    def test_check_field_valid(self):
        """Check field returns an empty response if the form is valid."""
        url = reverse("check_field", args=["username"])
        response = self.client.get(
            url, {"username": "validuser", "email": "valid@example.com"}
        )
        self.assertContains(response, "messages", count=0)

    def test_check_field_invalid(self):
        """Check field returns error messages if the form is invalid."""
        url = reverse("check_field", args=["email"])
        response = self.client.get(url, {"username": "", "email": "invalid"})
        self.assertContains(response, "errors")
