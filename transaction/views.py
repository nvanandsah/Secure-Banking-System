from django.shortcuts import render, redirect
from .forms import trnsction,addMoney,debitMoney,transferMerch
from django.contrib.auth.decorators import login_required
from .models import TX_in,TX_merchant
from random import randint
import pyotp
import datetime
from login.models import User
from django.db.models import SET_NULL, CASCADE
from django.contrib import messages


def transactionMerch(request):
    if not request.user.is_authenticated:
        return redirect("home")
    if request.user.designation!="merchant":
        return redirect("ihome")
    print("Right place")
    form=transferMerch(request.POST or None)
    title="Merchant Transaction"
    if form.is_valid():
        from_acc_no = form.cleaned_data.get("from_acc_no")
        to_acc_no = form.cleaned_data.get("to_acc_no")
        full_name=form.cleaned_data.get("full_name")
        amount=form.cleaned_data.get("Amount")
        if amount<1:
            context = {"form": form,
                        "title": title,
                        "message":"ENter valid amount"
                }
            return render(request, "transaction/tr_page.html", context)
        
        if from_acc_no==request.user.acc_no or to_acc_no==request.user.acc_no:
            context = {"form": form,
                        "title": title,
                        "message":"Cant transfer to your account"
                }
            return render(request, "transaction/tr_page.html", context)
        if full_name!=request.user.full_name:
            context = {"form": form,
                        "title": title,
                        "message":"Incorrect name"
                }
            return render(request, "transaction/tr_page.html", context)


        count=User.objects.filter(acc_no=from_acc_no).count()
        if count==0:
                context = {"message": 'Error : Account number entered doesnt exist',
                            "form": form,
                            "title": title,                   
                    }
                return render(request,"transaction/tr_page.html", context)
        userN=User.objects.filter(acc_no=from_acc_no)[0]
        if userN.designation=="manager" or userN.designation=="employee" or userN.designation=="admin":
            context = {"message": 'Error : Transaction not allowed in this account',
                        "form": form,
                        "title": title,                  
                }
            return render(request,"transaction/tr_page.html", context)

                

        
        count=User.objects.filter(acc_no=to_acc_no).count()
        if count==0:
                context = {"message": 'Error : Account number entered doesnt exist',
                            "form": form,
                            "title": title,                   
                    }
                return render(request,"transaction/tr_page.html", context)
        userN=User.objects.filter(acc_no=to_acc_no)[0]
        if userN.designation=="manager" or userN.designation=="employee" or userN.designation=="admin":
            context = {"message": 'Error : Transaction not allowed in this account',
                        "form": form,
                        "title": title,                  
                }
            return render(request,"transaction/tr_page.html", context)
        
        message = form.cleaned_data.get('message')
        txn=TX_merchant(full_name=full_name,from_acc_no=from_acc_no,to_acc_no=to_acc_no,Amount=amount,message=message,m_acc_no=request.user.acc_no)
        txn.save()
        return redirect("ihome")
    context = {"form": form,
                   "title": title
                   }
    return render(request, "transaction/tr_page.html", context)

def approve_merch_req(request,txID):
    if not request.user.is_authenticated:
        return redirect("home")
    if request.user.designation!="user" and request.user.designation!="merchant" :
        return redirect("home")
    tx=TX_merchant.objects.filter(id=txID)[0]
    if tx.status!="3":
        return redirect("home")
    tx=TX_merchant.objects.filter(id=txID)[0]
    if tx.from_acc_no!=request.user.acc_no:
        return "home"
    ToUser=User.objects.filter(acc_no=tx.to_acc_no)[0]
    start_transact(request,request.user,ToUser.full_name,"3",tx.to_acc_no,tx.Amount,tx.message,000000)
    TX_merchant.objects.filter(id=txID).update(status="1")
    return redirect("home")

def decline_merch_req(request,txID):
    if not request.user.is_authenticated:
        return redirect("home")
    if request.user.designation!="user" and request.user.designation!="manager" :
        return redirect("home")
    tx=TX_merchant.objects.filter(id=txID)[0]
    if tx.status!="3":
        return redirect("home")
    if tx.from_acc_no!=request.user.acc_no:
        return "home"
    TX_merchant.objects.filter(id=txID).update(status="2")
    return redirect("home")
    
    
     
@login_required()
def trnsac(request):
    if not request.user.is_authenticated:
        return redirect("home")
    else:
        if request.user.designation!="user" and request.user.designation!="merchant":
            return redirect("home")
        title = "Transaction "
        form = trnsction(request.POST or None)
        if form.is_valid():
            account_no = form.cleaned_data.get("acc_no")
            r_name=form.cleaned_data.get("full_name")
            amount=form.cleaned_data.get("Amount")
            if amount<1:
                context = {"form": form,
                            "title": title,
                            "message":"ENter valid amount"
                    }
                return render(request, "transaction/tr_page.html", context)
            message = form.cleaned_data.get('message')
            ammount_user=request.user.balance
           # print("ACC_NO"+int(account_no))
            OTP = form.cleaned_data.get("OTP")
            Userlog = request.user
            totp = pyotp.TOTP(Userlog.OTPSeed)
            print("Current OTP:", totp.now())
            count=User.objects.filter(acc_no=account_no).count()
            if count==0:
                context = {"message": 'Error : Account number entered doesnt exist',
                            "form": form,
                            "title": title,                   
                    }
                return render(request,"transaction/tr_page.html", context)
            userN=User.objects.filter(acc_no=account_no)[0]
            if userN.designation=="manager" or userN.designation=="employee" or userN.designation=="admin":
                context = {"message": 'Error : Transaction not allowed in this account',
                            "form": form,
                            "title": title,                  
                    }
                return render(request,"transaction/tr_page.html", context)
            if userN.full_name!=r_name:
                context = {"message": 'Error : Name not matched',
                            "form": form,
                            "title": title,                  
                    }
                return render(request,"transaction/tr_page.html", context)
            if account_no==request.user.acc_no:
                context = {"message": 'Error : Cant transfer to your own account',
                            "form": form,
                            "title": title,                  
                    }
                return render(request,"transaction/tr_page.html", context)

            if not Userlog.verify_otp(OTP):
                print('Invalid OTP')
                context = {"form": form,
                            "title": title,
                            "message":"Invalid OTP"
                    }
                return render(request, "transaction/tr_page.html", context)
            else:
                if(ammount_user>amount):
                    print('transaction possible')
                    #request.user.balance = request.user.balance - ammount
                    context = {"message": ' Transaction successful',
                            "name" : request.user.full_name,
                            "Acc" :  request.user.acc_no,
                            "bal" :request.user.balance
                    }
                    start_transact(request,request.user,r_name,"3",account_no,amount,message,OTP)  
                    return render(request,"transaction/addedmoney.html", context)
                else:
                    print('insuffiecient balance')
                    context = {"message": 'Error : Insufficient Balance',
                            "name" : request.user.full_name,
                            "Acc" :  request.user.acc_no,
                            "bal" :ammount_user,                 
                    }
                    return render(request,"transaction/addedmoney.html", context)
        context = {"form": form,
                   "title": title
                   }
        return render(request, "transaction/tr_page.html", context)
    

@login_required()
def add_money(request): #2
    if not request.user.is_authenticated:
        return redirect("home")
    else:
        if request.user.designation!="user" and  request.user.designation!="merchant":
            return redirect("home")
        title = "Add Money "
        form = addMoney(request.POST or None)
        if form.is_valid():
            account_no = form.cleaned_data.get("acc_no")
            amount=form.cleaned_data.get("Amount")
            message = form.cleaned_data.get('message')
            if amount<1:
                context = {"form": form,
                            "title": title,
                            "message":"ENter valid amount"
                    }
                return render(request, "transaction/addmoney_own.html", context)
            ammount_user=request.user.balance
            #makepay=request.user.do_transaction(0,amount)
            if (account_no==request.user.acc_no):
                OTP = form.cleaned_data.get("OTP")
                Userlog = request.user
                totp = pyotp.TOTP(Userlog.OTPSeed)
                print("Current OTP:", totp.now())
                if not Userlog.verify_otp(OTP):
                    print('Invalid OTP')
                    context = {"form": form,
                            "title": title,
                            "message":"Invalid OTP"
                    }
                    return render(request, "transaction/addmoney_own.html", context)
                else:
                    start_transact(request,request.user,request.user.full_name,"2",account_no,amount,message,OTP)
                    context = {"message": 'Pls wait 24hrs to complete transaction',
                            "Acc" : request.user.acc_no,
                            "bal" :ammount_user
                     }

                    return redirect("home")
            
            
            else:
                context = {"form": form,
                            "title": title,
                            "message":"ENter valid acc_no"
                    }
                return render(request, "transaction/addmoney_own.html", context)
        context = {"form": form,
                   "title": title
                   }
        return render(request, "transaction/addmoney_own.html", context)

        
@login_required()
def debit_money(request): #1
    if not request.user.is_authenticated:
        return redirect("home")
    else:
        if request.user.designation!="user" and request.user.designation!="merchant":
            return redirect("home")
        title = "Debit Money "
        form = debitMoney(request.POST or None)
        if form.is_valid():
            account_no = form.cleaned_data.get("acc_no")
            amount=form.cleaned_data.get("Amount")
            if amount<1:
                context = {"form": form,
                            "title": title,
                            "message":"ENter valid amount"
                    }
                return render(request, "transaction/debitmoney.html", context)
            message = form.cleaned_data.get('message')
            ammount_user=request.user.balance
            #makepay=request.user.do_transaction(0,amount)
            if (account_no==request.user.acc_no):
                if(ammount_user > amount):
                    OTP = form.cleaned_data.get("OTP")
                    Userlog = request.user
                    totp = pyotp.TOTP(Userlog.OTPSeed)
                    print("Current OTP:", totp.now())
                    if not Userlog.verify_otp(OTP):
                        print('Invalid OTP')
                        context = {"form": form,
                            "title": title,
                            "message":"Invalid OTP"
                        }
                        return render(request, "transaction/debitmoney.html", context)
                    else:
                        start_transact(request,request.user,request.user.full_name,"1",account_no,amount,message,OTP)
                        context = {"message": 'Pls wait 24hrs to complete transaction',
                            "Acc" : request.user.acc_no,
                            "bal" :ammount_user
                        }
                        return redirect("home")
                else:
                    print('insuffiecient balance')
                    context = {"message": 'Error : Insufficient Balance',
                            "name" : request.user.full_name,
                            "Acc" :  request.user.acc_no,
                            "bal" :ammount_user
                    }
            #return redirect("home")
                    return render(request,"transaction/bal_insuff.html", context)
            

            else:    
                context = {"form": form,
                            "title": title,
                            "message":"ENter valid acc_no"
                    }
                return render(request, "transaction/debitmoney.html", context)
        context = {"form": form,
                            "title": title,
                    }
        return render(request, "transaction/debitmoney.html", context)

def start_transact(request,user, to_name , Tr_type, to_acc_no, ammount,message,OTP):
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
                                                OTP=OTP
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
                                                OTP=OTP
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
                                messages.info(request, "Can't transfer to same account")
                                print("Can't transfer to same account")
                            else:
                                transactions = TX_in(fromUser = from_acc, toUser = to_acc, status='3',
                                                full_name= to_acc.full_name, acc_no= to_acc.acc_no,
                                                is_cash=False,
                                                Amount=ammount,
                                                creation_time=currentDT,
                                                message=message,
                                                Tr_type="3",
                                                OTP=OTP
                                                 )
                                transactions.save()
                        else:
                            print("Name conflict ")
                            messages.info(request, "Name conflict ")

