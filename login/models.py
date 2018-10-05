from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator
    )
# Create your models here.
from .managers import UserManager
REGEX = '^[a-zA-Z ]*$'

G_CHOICE = (
    ("Male", "Male"),
    ("Female", "Female"),
    )


class User(AbstractUser):
#class User():
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
    gender = models.CharField(max_length=6, choices=G_CHOICE)
    email = models.EmailField(unique=True, blank=False)
    contact_no = models.IntegerField(unique=True)
    Address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
        )
    objects = UserManager()

    USERNAME_FIELD = 'email'  # use email to log in
    REQUIRED_FIELDS = []  # required when user is created

    def __str__(self):
        return str(self.acc_no)
