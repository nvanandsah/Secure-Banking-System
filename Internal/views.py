from django.shortcuts import render, redirect
from django.contrib import messages
from login.forms import UserRegistrationForm, UserLoginForm
from .forms import modifyacc
from login.models import User
from django.db.models import Max
from django.contrib.auth import (authenticate,
                                 login,
                                 logout
                                 )
from django.shortcuts import render
from transaction.models import TX_in



def get_from_tuple(my_tuple, key):
    try:
        return next(y for x, y in my_tuple if x == key)
    except StopIteration:
        return None

# Create your views here.
def home(request):
	#print("Here in Employee"+request.user.is_authenticated)
	#print(request.user.email)
	#print(request.user.acc_no)
    if not (request.user.is_authenticated):
        return render(request,"base/home.html",{})
    else:
        arr = TX_in.objects.all()
        #print(arr)
        for i in arr:
            i.status=get_from_tuple(TX_in.STATUS, i.status)
        return render(request,"base/loggedInEmployee.html",{'name' : request.user.email,'trns':arr})

# Create your views here.
def account_handling(request):
    if not (request.user.is_authenticated):
        return render(request,"base/home.html",{})
    else:
        arr = User.objects.all()
        return render(request,"base/account.html",{'name' : request.user ,'arr':arr })

def delete_acc(request,UserID):
    User.objects.filter(id=UserID).delete()
    print(UserID)
    return redirect("iaccount_handling")


def modify_acc(request,UserID):
    title = "Modify Account "
    Userlog=User.objects.filter(id=UserID)
    fullname=""
    email=""
    contact=0
    addr=""
    city=""
    for i in Userlog:

        fullname=i.full_name
        email=i.email
        addr=i.Address
        contact=i.contact_no
        city=i.city
  
    form = modifyacc(request.POST or None,initial={'full_name':fullname,'email':email,'Address':addr, 'contact_no':contact ,'city':city })
    if form.is_valid():
        full_name = form.cleaned_data.get('full_name')
        email = form.cleaned_data.get('email')
        contact_no=form.cleaned_data.get("contact_no")
        Address=form.cleaned_data.get("Address")
        city=form.cleaned_data.get("city")
        print(UserID)
        User.objects.filter(id=UserID).update(full_name=full_name,email=email,contact_no=contact_no,Address=Address,city=city)
        return redirect("iaccount_handling")
    context = {"form": form,
                "title": title
                   }
    return render(request,"base/modify_acc.html",context)
    #return redirect("iaccount_handling")

def approve_transaction(request,txID):
    print(txID)
    arr = TX_in.objects.filter(id=txID)
    for i in arr:
        if(i.Tr_type=="1"):
            #debit
            fromUser=i.fromUser
            availableAmount=fromUser.balance
            amount=i.Amount
            if(amount>availableAmount):
                print("Trancsaction not possible, low balance")
                i.status="5"
            else:
                fromUser.balance=fromUser.balance-amount
                i.status="1"
            User.objects.filter(acc_no=fromUser.acc_no).update(balance=fromUser.balance)
            TX_in.objects.filter(id=txID).update(status=i.status)
        if(i.Tr_type=="2"):
            fromUser=i.fromUser
            availableAmount=fromUser.balance
            amount=i.Amount
            fromUser.balance=fromUser.balance+amount
            i.status="1"
            User.objects.filter(acc_no=fromUser.acc_no).update(balance=fromUser.balance)
            TX_in.objects.filter(id=txID).update(status=i.status)
        
        if(i.Tr_type=="3"):
            fromUser=i.fromUser
            toUser=i.toUser
            availableAmount=fromUser.balance
            amount=i.Amount
            if(amount>availableAmount):
                print("Trancsaction not possible, low balance")
                i.status="5"
            else:
                fromUser.balance=fromUser.balance-amount
                toUser.balance=toUser.balance+amount
                i.status="1"
            User.objects.filter(acc_no=fromUser.acc_no).update(balance=fromUser.balance)
            User.objects.filter(acc_no=toUser.acc_no).update(balance=toUser.balance)
            TX_in.objects.filter(id=txID).update(status=i.status)
    return redirect("ihome")

def decline_transaction(request,txID):
    TX_in.objects.filter(id=txID).update(status="4")
    return redirect("ihome")
                    



    
def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Create an Internal User Bank Account"
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            print("mc")
            user.save()
            email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
            user = authenticate(username=email, password=password)
            print(user)
            #return render(request,"base/loggedin.html",{'name':email, 'Acc':user.acc_no,'Pass':password})
            return redirect("home")
        else:
            print(form.is_valid())
        context = {"title": title, "form": form}
        return render(request,"login/form.html",context)


def _login(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Login "
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            account_no = form.cleaned_data.get("acc_no")
            user_obj = User.objects.filter(acc_no=account_no)
            user_obj = user_obj.first()
            password = form.cleaned_data.get("password")
            user = authenticate(email=user_obj.email, password=password)
            login(request, user)
            messages.success(request, 'Welcome, {}!' .format(user.full_name))
            return redirect("home")
        context = {"form": form,
                   "title": title
                   }
        return render(request, "login/form.html", context)


'''def Int_Login(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:   ''' 




def logout_view(request):  
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        logout(request)
        return redirect("home")

