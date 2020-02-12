from django import forms
from .models import Members, Posts


class User(forms.ModelForm):
    class Meta:
        model = Members
        fields = ("firstname", "lastname", "email", "password",
                  'username', "gender", "city", "country","dateofbirth")
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password *'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email *'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firstname *'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lastname *'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username *'}),
            'dateofbirth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'gender': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'country': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Country *'
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'City *'
                }
            )
        }


class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=('attachment','postcontent')