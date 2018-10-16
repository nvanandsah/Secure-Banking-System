from django.shortcuts import render, redirect
from .forms import trnsction,addMoney
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import TX_in

@login_required()
def transaction(request):
    if not (request.user.is_authenticated):
        return render(request,"base/home.html",{})
    else:
        return redirect("transfer")

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
                TX_in.start_transact(request.user,r_name,"3",account_no,amount,message)

                
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
            account_no = form.cleaned_data.get("Account_No")
            amount=form.cleaned_data.get("Amount")
            message = form.cleaned_data.get('message')
            ammount_user=request.user.balance
            makepay=request.user.do_transaction(0,amount)
            context = {"message": 'Pls wait 24hrs to complete transaction',
                        "Acc" : request.user.acc_no,
                        "bal" :ammount_user
                    }
            return render(request, "transaction/addedmoney.html", context)
        context = {"form": form,
                   "title": title
                   }
        return render(request, "transaction/addmoney_own.html", context)


