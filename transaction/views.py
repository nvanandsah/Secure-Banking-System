from django.shortcuts import render, redirect
from .forms import trnsction
# Create your views here.
def transaction(request):
    if not (request.user.is_authenticated):
        return render(request,"base/home.html",{})
    else:
        return redirect("transfer")

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
            return redirect("home")
        context = {"form": form,
                   "title": title
                   }
        return render(request, "transaction/tr_page.html", context)

