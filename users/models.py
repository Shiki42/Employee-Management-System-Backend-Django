from django.db import models
from django.contrib.auth.models import AbstractUser
# Assuming you have a User model defined elsewhere for the creator field

class Profile(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('i do not wish to answer', 'I do not wish to answer'),
    ]

    CITIZENSHIP_CHOICES = [
        ('citizen', 'Citizen'),
        ('green card', 'Green Card'),
        ('no', 'No'),
    ]

    WORK_AUTH_CHOICES = [
        ('H1-B', 'H1-B'),
        ('L2', 'L2'),
        ('F1(CPT/OPT)', 'F1(CPT/OPT)'),
        ('H4', 'H4'),
        ('Other', 'Other'),
        ('N/A', 'N/A'),
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    feedback = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    preferred_name = models.CharField(max_length=100, blank=True)
    building = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20)
    work_phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    ssn = models.CharField(max_length=11)
    dob = models.DateField()
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    citizenship = models.CharField(max_length=50, choices=CITIZENSHIP_CHOICES)
    work_auth_type = models.CharField(max_length=50, choices=WORK_AUTH_CHOICES)
    work_auth_start_date = models.DateField()
    work_auth_end_date = models.DateField()
    work_auth_other = models.CharField(max_length=100, blank=True)
    driver_license = models.ForeignKey(Document, related_name='profile_driver_license', on_delete=models.CASCADE)
    profile_picture = models.ForeignKey(Document, related_name='profile_profile_picture', on_delete=models.CASCADE)

class VisaStatus(models.Model):
    DOC_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('N/A', 'N/A'),
        ('need to upload', 'Need to Upload'),
    ]

    status = models.CharField(max_length=50, choices=DOC_STATUS_CHOICES, default='N/A')
    doc_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('HR', 'HR'),
        ('admin', 'Admin'),
    ]

    VISA_STATUS_CHOICES = [
        ('optReceipt', 'OPT Receipt'),
        ('optEad', 'OPT EAD'),
        ('i983', 'I983'),
        ('i20', 'I20'),
        ('approved', 'Approved'),
    ]

    DOC_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('N/A', 'N/A'),
        ('need to upload', 'Need to Upload'),
    ]

    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='employee')
    password = models.CharField(max_length=255)  # Consider using Django's built-in password management
    application = models.ForeignKey('Application', on_delete=models.SET_NULL, null=True, blank=True)
    profile = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True)
    documents = models.ManyToManyField('Document')
    work_auth_type = models.CharField(max_length=50, choices=User.WORK_AUTH_CHOICES, blank=True)
    work_auth_start_date = models.DateField(null=True, blank=True)
    work_auth_end_date = models.DateField(null=True, blank=True)
    work_auth_other = models.CharField(max_length=100, blank=True)

    opt_receipt = models.OneToOneField(VisaStatus, on_delete=models.SET_NULL, null=True, related_name='opt_receipt')
    opt_ead = models.OneToOneField(VisaStatus, on_delete=models.SET_NULL, null=True, related_name='opt_ead')
    i983 = models.OneToOneField(VisaStatus, on_delete=models.SET_NULL, null=True, related_name='i983')
    i20 = models.OneToOneField(VisaStatus, on_delete=models.SET_NULL, null=True, related_name='i20')