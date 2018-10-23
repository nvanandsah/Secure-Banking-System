from django.shortcuts import render, redirect
from .forms import trnsction,addMoney,debitMoney
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import TX_in
import datetime
from login.models import User
from django.db.models import SET_NULL, CASCADE
from django.contrib import messages
@login_required()
def transaction(request):
    if not (request.user.is_authenticated):
        return render(request,"base/home.html",{})
    else:
        context = {
                        "name" : request.user.full_name,
                        "Acc" :  request.user.acc_no,
                        "bal" :request.user.balance,
                   
                   }
        return render(request, "transaction/transaction.html", context)
        

@login_required()
def trnsac(request):
    if not request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Transaction "
        form = trnsction(request.POST or None)
        if form.is_valid():
            account_no = form.cleaned_data.get("acc_no")
            r_name=form.cleaned_data.get("full_name")
            amount=form.cleaned_data.get("Amount")
            message = form.cleaned_data.get('message')
            ammount_user=request.user.balance
           # print("ACC_NO"+int(account_no))
            
            if(ammount_user>amount):
                print('transaction possible')
                #request.user.balance = request.user.balance - ammount
                context = {"message": ' Khush hoja',
                        "name" : request.user.full_name,
                        "Acc" :  request.user.acc_no,
                        "bal" :request.user.balance
                   }
                start_transact(request,request.user,r_name,"3",account_no,amount,message)

                
            else:
                print('insuffiecient balance')
                context = {"message": 'Error : Insufficient Balance',
                        "name" : request.user.full_name,
                        "Acc" :  request.user.acc_no,
                        "bal" :ammount_user
                   
                   }

            #return redirect("home")
                return render(request,"transaction/bal_insuff.html", context)
        context = {"form": form,
                   "title": title
                   }
        return render(request, "transaction/tr_page.html", context)
    

@login_required()
def add_money(request):
    if not request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Add Money "
        form = addMoney(request.POST or None)
        if form.is_valid():
            account_no = form.cleaned_data.get("acc_No")
            amount=form.cleaned_data.get("Amount")
            message = form.cleaned_data.get('message')
            ammount_user=request.user.balance
            #makepay=request.user.do_transaction(0,amount)
            start_transact(request,request.user,request.user.full_name,"2",account_no,amount,message)
            context = {"message": 'Pls wait 24hrs to complete transaction',
                        "Acc" : request.user.acc_no,
                        "bal" :ammount_user

                    }

            return redirect("home")
        context = {"form": form,
                   "title": title
                   }
        return render(request, "transaction/addmoney_own.html", context)


@login_required()
def debit_money(request):
    if not request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Debit Money "
        form = debitMoney(request.POST or None)
        if form.is_valid():
            account_no = form.cleaned_data.get("acc_No")
            amount=form.cleaned_data.get("Amount")
            message = form.cleaned_data.get('message')
            ammount_user=request.user.balance
            #makepay=request.user.do_transaction(0,amount)
            if(ammount_user > amount):
                start_transact(request,request.user,request.user.full_name,"1",account_no,amount,message)
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
                
        context = {"form": form,
                   "title": title
                   }
        return render(request, "transaction/debitmoney.html", context)

def start_transact(request,user, to_name , Tr_type, to_acc_no, ammount,message):
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
                                                 )
                                transactions.save()
                        else:
                            print("Name conflict ")
                            messages.info(request, "Name conflict ")

