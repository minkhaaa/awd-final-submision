from django.db import models

from accounts.models import Teacher


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="courses"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=255)
    body = models.TextField()
    attachment = models.FileField(upload_to="attachments/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
