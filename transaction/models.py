from django.db import models
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator
    )

REGEX = '^[a-zA-Z ]*$'
# Create your models here.

REGEX = '^[a-zA-Z ]*$'
class transaction(models.Model):
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
        Amount = models.PositiveIntegerField(
                validators=[
                    MinValueValidator(1000),
                    MaxValueValidator(100000)
<<<<<<< HEAD
                   
=======
>>>>>>> 24a59c7d0ec26e8ba952e1caeb3b6b27a644416f
                ]
        )
        message = models.CharField(
                max_length=256,
                validators=[
                        RegexValidator(
                            regex=REGEX,
                            message='Messages must be Alphabetic',
                            code='invalid_message_name'
                            )
                        ]
        )
        '''       trnsID = models.PositiveIntegerField(
                unique=True,
                validators=[
                    MinValueValidator(0),
                    MaxValueValidator(99999999)
                    ]            
        )'''