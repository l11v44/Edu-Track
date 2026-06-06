from django import forms
from .models import *


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'slug', 'category', 'description', 'status', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title','content' , 'video_url']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
        }
        labels = {
            'video_url': 'YouTube Video URL',
        }
        help_texts = {
            'video_url': 'Paste the link to your YouTube video here.',
        }

