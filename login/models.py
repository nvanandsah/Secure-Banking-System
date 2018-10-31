from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator
    )
import base64
import pyotp
# Create your models here.
from .managers import UserManager
REGEX = '^[a-zA-Z ]*$'
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
G_CHOICE = (
    ("Male", "Male"),
    ("Female", "Female"),
    )
D_CHOICE = (
			("user", "User: permission to do account operations"),
			("merchant", "Merchant:create payments for their users"),
			("employee", "Employee: check the employee dashboard"),
			("manager", "Manager : Manager/Staff, critical transactions"),
			("admin", "admin"),
		)

   
class User(AbstractUser):
    username = None
    full_name = models.CharField(
        max_length=256,
        blank=False,
        validators=[
                RegexValidator(
                    regex=REGEX,
                    message='Name must be Alphabetic',
                    code='invalid_full_name'
                    )
                ]
        )
    acc_no = models.PositiveIntegerField(
        unique=True,
        validators=[
            MinValueValidator(10000000),
            MaxValueValidator(99999999)
            ]
        )
    OTPSeed = models.CharField(max_length=16, validators=[alphanumeric], editable=False)
    gender = models.CharField(max_length=6, choices=G_CHOICE)
    email = models.EmailField(unique=True, blank=False)
    contact_no = models.IntegerField(unique=True)
    Address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    balance = models.DecimalField(
        default=1001,
        max_digits=12,
        decimal_places=2
        )
    objects = UserManager()
    STATUS = (
            ('O', "Active"),
            ('S', "Suspended"),
        )
    status = models.CharField(max_length=1, choices=STATUS,default="O")
    linked=models.CharField(max_length=1000, choices=STATUS,default="O")
    designation = models.CharField(max_length=25, choices=D_CHOICE)
    USERNAME_FIELD = 'email'  # use email to log in
    REQUIRED_FIELDS = []  # required when user is created

    def __str__(self):
        return str(self.acc_no)

    def regenerate_OTPseed(self):
        self.OTPSeed = pyotp.random_base32()
        print(self.OTPSeed)
        self.save()
        return self.OTPSeed,pyotp.totp.TOTP(self.OTPSeed).provisioning_uri("alice@google.com", issuer_name="Secure App")
        #return self.OTPSeed

    def verify_otp(self, otp):
        #if len(self.OTPSeed) != 16:
            #raise BankingException('Invalid OTP State, authenticate again.')
        totp = pyotp.TOTP((self.OTPSeed))
        print(self.OTPSeed)
        return totp.verify(otp)
    



