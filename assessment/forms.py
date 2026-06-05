from django import forms
from .models import *

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'instructions']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'instructions': forms.Textarea(attrs={'class':'form-control'}),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['text_content', 'file']
        widgets = {
            'text_content': forms.Textarea(attrs={'class':'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class':'form-control'}),
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['score' , 'feedback']
        widgets = {
            'score': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none',
                'placeholder': '0 - 100',
                'min': '0',
                'max': '100'
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all outline-none h-32 resize-none',
                'placeholder': 'Leave your feedback here...'
            }),
        }