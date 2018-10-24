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
D_CHOICE = (
			("user", "permission to do account operations"),
			("merchant", "create payments for their users"),
			("employee", "check the employee dashboard"),
			("manager", "Manager/Staff, critical transactions"),
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
    OTPSeed = models.PositiveIntegerField(
        unique=True,
        validators=[
            MinValueValidator(100000),
            MaxValueValidator(999999)
            ]
        )
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
    designation = models.CharField(max_length=25, choices=D_CHOICE)
    USERNAME_FIELD = 'email'  # use email to log in
    REQUIRED_FIELDS = []  # required when user is created

    def __str__(self):
        return str(self.acc_no)

    def do_transaction(self, transaction_type, amount, transaction, commit=True):
            if amount <= 0:
                raise BankingException('Invalid Amount')
            if transaction is None or transaction.amount != amount and transaction.status != 'A':
                raise BankingException('Security Error')
            if transaction_type == '1':
                self.balance -= amount
            if transaction_type == '2':
                self.balance += amount
            if self.balance < 0:
                raise BankingException('Security Error')
            if commit:
                self.save()



