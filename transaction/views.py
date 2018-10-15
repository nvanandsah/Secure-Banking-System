from django.shortcuts import render, redirect
from .forms import trnsction
from django.contrib.auth.decorators import login_required
# Create your views here.

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
            account_no = form.cleaned_data.get("Account_No")
            r_name=form.cleaned_data.get("Name")
            amount=form.cleaned_data.get("Amount")
            message = form.cleaned_data.get('message')
            ammount_user=request.user.balance
            
            if(ammount_user>amount):
                print('transaction possible')
            else:
                print('insuffiecient balance')
<<<<<<< HEAD
              
            return redirect("home")
=======

            #return redirect("home")
            context = {"message": 'Error : Insufficient Balance',
                        "name" : request.user.full_name,
                        "Acc" :  request.user.acc_no,
                        "bal" :ammount_user
                   
                   }
            return render(request,"transaction/bal_insuff.html", context)
>>>>>>> 24a59c7d0ec26e8ba952e1caeb3b6b27a644416f
        context = {"form": form,
                   "title": title
                   }
        return render(request, "transaction/tr_page.html", context)

