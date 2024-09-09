import factory
from django.contrib.auth import get_user_model

from accounts.models import StatusUpdate, Student, Teacher
from courses.models import Course, Enrollment, Rating, Topic


# User Factory
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    is_student = False
    is_teacher = False
    password = factory.PostGenerationMethodCall("set_password", "testpass")


# Student Factory
class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory, is_student=True)


# Teacher Factory
class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teacher

    user = factory.SubFactory(UserFactory, is_teacher=True)


# Course Factory
class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.Faker("sentence")
    description = factory.Faker("paragraph")
    instructor = factory.SubFactory(TeacherFactory)


# Enrollment Factory
class EnrollmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Enrollment

    user = factory.SubFactory(StudentFactory)
    course = factory.SubFactory(CourseFactory)


# Rating Factory
class RatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rating

    user = factory.SubFactory(StudentFactory)
    course = factory.SubFactory(CourseFactory)
    rating = factory.Faker("random_int", min=1, max=5)
    comment = factory.Faker("sentence")


# Topic Factory
class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topic

    course = factory.SubFactory(CourseFactory)
    title = factory.Faker("sentence")
    body = factory.Faker("paragraph")
