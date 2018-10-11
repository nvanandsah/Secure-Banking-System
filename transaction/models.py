from django.db import models
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator
    )
# Create your models here.
class transaction():
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