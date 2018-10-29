from __future__ import unicode_literals
from django.db import models
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator
    )

# Create your models here.
REGEX = '^[a-zA-Z ]*$'
alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

class ModifiedUser(models.Model):
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
        validators=[
            MinValueValidator(10000000),
            MaxValueValidator(99999999)
            ]
        )
    email = models.EmailField(unique=True, blank=False)
    contact_no = models.IntegerField(unique=True)
    Address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    isModified=models.CharField(max_length=1,default="0")
    def __str__(self):
        return str(self.acc_no)

