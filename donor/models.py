from django.db import models


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

    def __str__(self):
        return f"{self.name} ({self.blood_group})"

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

    def __str__(self):
        return f"{self.name} ({self.blood_group})"

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

    def __str__(self):
        return f"{self.name} ({self.blood_group})"

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

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Payment(models.Model):
    purpose_choices = (
        ("Donation", "Donation"),
        ("Membership", "Membership"),
        ("Campaign", "Campaign"),
        ("Emergency Support", "Emergency Support"),
    )
    method_choices = (
        ("Cash", "Cash"),
        ("Bank Transfer", "Bank Transfer"),
        ("eSewa", "eSewa"),
        ("Khalti", "Khalti"),
    )
    status_choices = (
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    )

    donor_name = models.CharField(max_length=70)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=30, choices=purpose_choices)
    payment_method = models.CharField(max_length=30, choices=method_choices)
    status = models.CharField(max_length=20, choices=status_choices, default="Completed")
    transaction_id = models.CharField(max_length=40, unique=True)
    remarks = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payment"

    def __str__(self):
        return f"{self.donor_name} - {self.amount}"
