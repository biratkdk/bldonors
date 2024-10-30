from django import db
from django.db import models

# Create your models here.
class Donor(models.Model):
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=100)
    phone = models.IntegerField()
    address = models.CharField(max_length=70)
    age = models.IntegerField()
    quantity = models.IntegerField()
    gender_choices =(
    ("Male","Male"),
    ("Female","Female"),
    ("Other","Other"),
    )
    gender=models.CharField(max_length=10,choices=gender_choices)
    blood_choices=(
    ("O Positive","O Positive"),
    ("O Negative","O Negative"),
    ("A Positive","A Positive"),
    ("A Negative","A Negative"),
    ("B Positive","B Positive"),
    ("B Negative","B Negative"),
    ("AB Positive","AB Positive"),
    ("AB Negative","AB Negative"),
    )
    blood_group=models.CharField(max_length=50,choices=blood_choices)
    class Meta :
        db_table = "donor"

class Bloodreq(models.Model):
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=100)
    phone = models.IntegerField()
    address = models.CharField(max_length=70)
    age = models.IntegerField()
    quantity = models.IntegerField()
    gender_choices =(
    ("Male","Male"),
    ("Female","Female"),
    ("Other","Other"),
    )
    gender=models.CharField(max_length=10,choices=gender_choices)
    blood_choices=(
    ("O Positive","O Positive"),
    ("O Negative","O Negative"),
    ("A Positive","A Positive"),
    ("A Negative","A Negative"),
    ("B Positive","B Positive"),
    ("B Negative","B Negative"),
    ("AB Positive","AB Positive"),
    ("AB Negative","AB Negative"),
    )
    blood_group=models.CharField(max_length=50,choices=blood_choices)
    class Meta:
        db_table = "bloodreq"

class Stock(models.Model):
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=100)
    phone = models.IntegerField()
    address = models.CharField(max_length=70)
    quantity = models.IntegerField()
    gender_choices =(
    ("Male","Male"),
    ("Female","Female"),
    ("Other","Other"),
    )
    gender=models.CharField(max_length=10,choices=gender_choices)
    blood_choices=(
    ("O Positive","O Positive"),
    ("O Negative","O Negative"),
    ("A Positive","A Positive"),
    ("A Negative","A Negative"),
    ("B Positive","B Positive"),
    ("B Negative","B Negative"),
    ("AB Positive","AB Positive"),
    ("AB Negative","AB Negative"),
    )
    blood_group=models.CharField(max_length=50,choices=blood_choices)
    class Meta:
        db_table = "stock"

class Contact(models.Model):
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=100)
    subject_choices =(
    ("Donation","Donation"),
    ("Blood_Request","Blood_Request"),
    ("How_To_Use","How_to_Use"),
    ("Eligibility","Eligibility"),
    ("Terms&Conditions","Terms&conditions"),
    )
    subject=models.CharField(max_length=20,choices=subject_choices)
    message = models.TextField(max_length=70)
    class Meta:
        db_table = "contact"