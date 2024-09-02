from django import forms

from .models import Course, Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rating", "comment"]


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "w-full p-2 border border-gray-300 rounded"}
            ),
            "description": forms.Textarea(
                attrs={"class": "w-full p-2 border border-gray-300 rounded"}
            ),
        }
