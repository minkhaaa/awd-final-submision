from rest_framework import serializers

from accounts.models import StatusUpdate, User
from courses.models import Course, Enrollment, Rating, Topic


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_student", "is_teacher"]


# StatusUpdate Serializer
class StatusUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Show user info in the status update

    class Meta:
        model = StatusUpdate
        fields = ["id", "user", "content", "updated_at"]


# Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField()  # Show instructor's username

    class Meta:
        model = Course
        fields = ["id", "title", "description", "instructor", "created_at"]


# Topic Serializer
class TopicSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)  # Show course details in topic

    class Meta:
        model = Topic
        fields = ["id", "course", "title", "body", "attachment", "created_at"]


# Enrollment Serializer
class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Show user info in the enrollment
    course = CourseSerializer(read_only=True)  # Show course info

    class Meta:
        model = Enrollment
        fields = ["id", "user", "course", "enrolled_at"]


# Rating Serializer
class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Show user info
    course = CourseSerializer(read_only=True)  # Show course info

    class Meta:
        model = Rating
        fields = ["id", "user", "course", "rating", "comment", "rated_at"]
