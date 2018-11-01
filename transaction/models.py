from django.db import models
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator
    )
from django.db.models import Max
import datetime
from login.models import User
from django.db.models import SET_NULL, CASCADE
from django.contrib import messages
from login.managers import UserManager
REGEX = '^[a-zA-Z ]*$'
class TX_in(models.Model):
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
        Amount = models.PositiveIntegerField(
                validators=[
                    MinValueValidator(1),
                    MaxValueValidator(10000000)
                ]
        )
        OTP = models.PositiveIntegerField(
                validators=[
                    MinValueValidator(100000),
                    MaxValueValidator(999999)
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
        objects = UserManager()
        fromUser = models.ForeignKey(User,related_name="from_account", null=True, on_delete=SET_NULL, blank=True)
        toUser = models.ForeignKey(User, related_name="to_account", null=True, on_delete=SET_NULL, blank=True)
        STATUS = (
            ('1', "Approved"),
            ('2', "Payment/Cash"),
            ('3', "Processing"),
            ('4', "Rejection"),
            ('5', "Insufficient Balance"),
        )
        status = models.CharField(max_length=1, choices=STATUS, editable=False,default="3")
        Tr_type=models.CharField(max_length=1,default="1")
        is_cash = models.BooleanField(editable=False)
        creation_time = models.DateTimeField(auto_now_add=True)
       # last_changed_time = models.DateTimeField(auto_now=True)

        #@staticmethod

class TX_merchant(models.Model):
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
    m_acc_no=models.PositiveIntegerField(
                validators=[
                    MinValueValidator(10000000),
                    MaxValueValidator(99999999)
                    ],
                default=99999999
        )
    from_acc_no = models.PositiveIntegerField(
                validators=[
                    MinValueValidator(10000000),
                    MaxValueValidator(99999999)
                    ]
        )
    to_acc_no = models.PositiveIntegerField(
                validators=[
                    MinValueValidator(10000000),
                    MaxValueValidator(99999999)
                    ]
        )
    Amount = models.PositiveIntegerField(
                validators=[
                    MinValueValidator(1),
                    MaxValueValidator(10000000)
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
    STATUS = (
            ('1', "Approved"),
            ('2', "Rejected"),
            ('3', "Processing"),
    
        )
    status = models.CharField(max_length=1, choices=STATUS, editable=False,default="3")


        

                    





                                




