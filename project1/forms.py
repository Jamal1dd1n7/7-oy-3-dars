from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from .models import *


# Course Form
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'  # Include all fields in the model
        widgets = {
            'title': forms.TextInput(attrs={  # Use forms.TextInput for widgets
                "class": "form-control",  
                "placeholder": "Kurs nomini kiriting",  # Optional placeholder
            }),
            'description': forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Kurs haqida ma`lumot kiriting",
            })
        }
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Group Form
class GroupForm(forms.ModelForm):
    class Meta: 
        model = Group
        fields = ['title', 'teacher', 'course', 'student_count']
        widgets = {
            'title': forms.TextInput(attrs={
                "class": "form-control"
            }),
            'teacher': forms.TextInput(attrs={
                "class": "form-control"
            }),
            'course': forms.Select(attrs={  # Use Select widget for ModelChoiceField
                "class": "form-control"
            }),
            'student_count': forms.NumberInput(attrs={  # Use NumberInput for IntegerField
                "class": "form-control"
            }),
        }
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Lesson Form
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'teacher', 'content', 'group']
        widgets = {
            'title': forms.TextInput(attrs={
                "placeholder": "Nomi",
                "class": "form-control"
            }),
            'teacher': forms.TextInput(attrs={
                "placeholder": "O`qituvchi",
                "class": "form-control"
            }),
            'content': forms.Textarea(attrs={
                "placeholder": "Matni",
                "class": "form-control"
            }),
            'group': forms.Select(attrs={
                "class": "form-select"
            })
        }
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Register Form
class RegisterForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email']
        labels = {
            'username': "Foydalanuvchi nomi",
            'email': "Elektron pochta manzili"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': "form-control form-control-lg"})
        self.fields['email'].widget.attrs.update({'class': "form-control form-control-lg"})
        self.fields['password1'].widget.attrs.update({'class': "form-control form-control-lg"})
        self.fields['password2'].widget.attrs.update({'class': "form-control form-control-lg"})



# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Login Form:
class LoginForm(AuthenticationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        username = self.fields['username']
        password = self.fields['password']

        username.label = "Foydalanuvchi nomi"
        username.widget.attrs.update({
            'class': "form-control",
            'placeholder': "Foydalanuvchi nomingizni kiriting"
        })
        password.label = "Password kiriting"
        password.widget.attrs.update({
            'class': "form-control",
            'placeholder': "Parolingizni kiriting"
        })
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Comment Form:
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': "form-control"
            })
        }

    def save(self, comment, user, lesson):
        comment.objects.create(
            text=self.cleaned_data.get('text'),
            author=user,
            lesson=lesson
        )

    def update(self, value):
        value.text = self.cleaned_data.get('text')
        value.save()
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Message form:
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'message', 'to_user']  # Uchta maydon
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sarlavha kiriting'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Xabar matnini yozing'
            }),
            'to_user': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Qabul qiluvchi emailini kiriting'
            }),
        }
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------