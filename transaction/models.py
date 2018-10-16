from django.db import models
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator
    )
from login.models import User
from django.db.models import SET_NULL, CASCADE
REGEX = '^[a-zA-Z ]*$'
# Create your models here.
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
REGEX = '^[a-zA-Z ]*$'
class transaction(models.Model):
        fromUser = models.ForeignKey(User,related_name="from_account", null=True, on_delete=SET_NULL, blank=True)
        toUser = models.ForeignKey(User, related_name="to_account", null=True, on_delete=SET_NULL, blank=True)
        STATUS = (
            ('1', "Payment/Cash"),
            ('2', "Approved"),
            ('3', "Processing"),
            ('4', "Rejection"),
            ('5', "Insufficient_Balance"),
            ('6', "Error_Occured"),
        )
    #    status = models.CharField(max_length=1, choices=STATUS, editable=False)
        is_cash = models.BooleanField(editable=False)
        creation_time = models.DateTimeField(auto_now_add=True)
        last_changed_time = models.DateTimeField(auto_now=True)
        trnsID = models.PositiveIntegerField(
                unique=True,
                validators=[
                    MinValueValidator(0),
                    MaxValueValidator(99999999)
                    ]            
        )
        def start_transaction(self, user, to_name , Tr_type, from_acc_no, to_acc_no, ammount):
            from_acc = User.objects.filter(acc_no = int(from_acc_no.strip()))
            if(from_acc.len !=0 ):
                from_acc = from_acc[0]
                if(from_acc.acc_no != user.acc_no):
                    print("Doesn't belong to you")
                else:
                    to_acc = User.objects.filter(acc_no = int(to_acc_no.strip()))
                    if(to_acc != None):
                        if(to_acc.full_name == to_name):
                            if(to_acc.acc_no == user.acc_no and Tr_type==3):
                                print("Can't transfer to same account")
                            elif(to_acc.acc_no==user.acc_no):
                                user.do_transaction(Tr_type,ammount,self,False)
                            else:
                                kwarg = []
                                transactions = transaction(fromUser = from_acc, toUser = to_acc, status='3',
                                                full_name= to_acc.full_name, acc_no= to_acc.acc_no )




