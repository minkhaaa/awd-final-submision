from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Student, Teacher, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_teacher",
        "is_student",
    )
    list_filter = ("is_teacher", "is_student")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Roles", {"fields": ("is_teacher", "is_student")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_teacher and not Teacher.objects.filter(user=obj).exists():
            Teacher.objects.create(user=obj)
        if obj.is_student and not Student.objects.filter(user=obj).exists():
            Student.objects.create(user=obj)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("user",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user",)


# Register your models here.
