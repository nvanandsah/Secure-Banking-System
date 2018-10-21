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
        fromUser = models.ForeignKey(User,related_name="from_account", null=True, on_delete=SET_NULL, blank=True)
        toUser = models.ForeignKey(User, related_name="to_account", null=True, on_delete=SET_NULL, blank=True)
        STATUS = (
            ('1', "Approved"),
            ('2', "Payment/Cash"),
            ('3', "Processing"),
            ('4', "Rejection"),
            ('5', "Error_Occured"),
        )
        status = models.CharField(max_length=1, choices=STATUS, editable=False,default="3")
        Tr_type=models.CharField(max_length=1,default="1")
        is_cash = models.BooleanField(editable=False)
        creation_time = models.DateTimeField(auto_now_add=True)
       # last_changed_time = models.DateTimeField(auto_now=True)

        @staticmethod
        def start_transact(user, to_name , Tr_type, to_acc_no, ammount,message):
            if(Tr_type=='1'):
                from_acc = user
                if(from_acc!=None ):

                    currentDT = datetime.datetime.now()
                    transactions = TX_in(fromUser = from_acc, toUser = None, status='3',
                                                full_name= user.full_name, acc_no= from_acc.acc_no,
                                                is_cash=True,
                                                Amount=ammount,
                                                creation_time=currentDT,
                                                message=message,
                                                Tr_type="1",
                                                )
                    transactions.save()
            if(Tr_type=='2'):
                from_acc = user
                if(from_acc!=None ):
                    currentDT = datetime.datetime.now()
                    transactions = TX_in(fromUser = from_acc, toUser = None, status='3',
                                                full_name= user.full_name, acc_no= from_acc.acc_no,
                                                is_cash=True,
                                                Amount=ammount,
                                                creation_time=currentDT,
                                                message=message,
                                                Tr_type="2",
                                                )
                    transactions.save()
            
            if(Tr_type=='3'):
                from_acc = user
                if(from_acc!=None ):
                    currentDT = datetime.datetime.now()
                    to_acc = User.objects.filter(acc_no = to_acc_no)
              #      print("AccountNO"+to_acc_no)
                    to_acc=to_acc[0]
                    if(to_acc != None):
                        if(to_acc.full_name == to_name):
                            if(to_acc.acc_no == user.acc_no):
                                print("Can't transfer to same account")
                            else:
                                transactions = TX_in(fromUser = from_acc, toUser = to_acc, status='3',
                                                full_name= to_acc.full_name, acc_no= to_acc.acc_no,
                                                is_cash=False,
                                                Amount=ammount,
                                                creation_time=currentDT,
                                                message=message,
                                                Tr_type="3",
                                                 )
                                transactions.save()
                        else:
                            print("Name conflict ")

                    





                                




