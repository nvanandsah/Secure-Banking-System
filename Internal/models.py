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
D_CHOICE = (
    ("Employee", "Employee"),
    ("Sys. Admin", "SySAdmin"),
    ("Sys. Manager", "SySManager"),
    )
class IntUser(AbstractUser):
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
    email = models.EmailField(unique=True, blank=False)
    contact_no = models.IntegerField(unique=True)
    Address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    objects = UserManager()
    designation = models.CharField(max_length=11, choices=D_CHOICE)
    USERNAME_FIELD = 'email'  # use email to log in
    REQUIRED_FIELDS = []  # required when user is created

    def __str__(self):
        return str(self.full_name)




