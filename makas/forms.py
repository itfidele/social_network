from django import forms
from .models import Members, Posts,Comments
from .widgets import BootstrapDateTimePickerInput

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
        widgets = {
            'postcontent': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'rows':2,
                    'style':'border:2px solid skyblue;padding:10px;border-radius:10px;box-shadow:inset 5px 0px 10px 0px skyblue;',
                    'placeholder':'write your wish here...',
                }
            ),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=['comment']
        widgets={
            'comment':forms.Textarea(
                attrs={
                    'class':'form-control',
                }
            )
        }