from django.db import models

# Create your models here.

class Users(models.Model):
    GENDER_CHOICE=[
        ("M","Male"),
        ("F","Female"),
    ]
    COUNTRIES=[
        ("RW","Rwanda"),
        ("UG","Uganda"),
        ("BU","Burundi"),
        ("TZ","Tanzania"),
    ]
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=250)
    dateofbirth=models.DateField(blank=False)
    gender=models.CharField(max_length=1,choices=GENDER_CHOICE)
    city=models.CharField(max_length=200)
    country=models.CharField(max_length=3,choices=COUNTRIES)

    def __str__(self):
        return self.firstname
