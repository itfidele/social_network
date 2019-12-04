from django import forms
from .models import Users

class User(forms.ModelForm):
    class Meta:
        model = Users
        fields = ("firstname","lastname","email","password","dateofbirth","gender","city","country")
        widgets={
        'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password *'}),
        'email':forms.EmailInput(attrs={'class':'form-control'}),
        'firstname':forms.TextInput(attrs={'class':'form-control','placeholder':'Firstname *'}),
        'lastname':forms.TextInput(attrs={'class':'form-control','placeholder':'Lastname *'}),
        'dateofbirth':forms.SelectDateWidget(
            attrs={'class':'form-control'},
            years=range(2000,2019)
        ),
        'gender':forms.Select(
            attrs={'class':'form-control'}
        ),
        'country':forms.Select(
            attrs={
                'class':'form-control'
            }
        ),
        'city':forms.TextInput(
            attrs={
                'class':'form-control'
            }
        )
    }
