from django import forms
from .models import Members, Posts


class User(forms.ModelForm):
    class Meta:
        model = Members
        fields = ("firstname", "lastname", "email", "password", 'username', "gender", "city", "country")
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password *'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firstname *'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lastname *'}),
            'dateofbirth': forms.DateInput(attrs={
                'type': 'date'
            }),
            'gender': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'country': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }


