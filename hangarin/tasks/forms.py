from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'h-form-control', 'placeholder': 'Enter task title...'}),
            'description': forms.Textarea(attrs={'class': 'h-form-control', 'rows': 4}),
            'deadline': forms.DateTimeInput(attrs={'class': 'h-form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'h-form-control'}),
            'category': forms.Select(attrs={'class': 'h-form-control'}),
            'priority': forms.Select(attrs={'class': 'h-form-control'}),
        }