from django.shortcuts import render, redirect
from django.contrib import messages
from login.forms import UserRegistrationForm, UserLoginForm,EmployeeRegistrationForm
from Internal.forms import modifyacc,addacc
from login.models import User
from django.db.models import Max
from base.models import ModifiedUser
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
        if request.user.designation=="user":
            return redirect("home")
        if request.user.designation=="admin":
            return redirect("iaccount_handling")
        if request.user.designation=="merchant":
            return redirect("homeMerchant")
        if request.user.designation=="employee":
            arr=TX_in.objects.filter(Amount__lte=100000)
        else:
            arr = TX_in.objects.all()
        #print(arr)
        CHOICE = (
    		("1", "Debit"),
    		("2", "Credit"),
			("3", "Transfer"),
    	)
        print(arr)
        print(request.user.id)
        for i in arr:
            i.status=get_from_tuple(TX_in.STATUS, i.status)
            i.Tr_type=get_from_tuple(CHOICE, i.Tr_type)
        return render(request,"base/loggedInEmployee.html",{'name' : request.user,'trns':arr})

# Create your views here.
def account_handling(request):
    if not (request.user.is_authenticated ):
        return render(request,"base/home.html",{})
    else:
        if request.user.designation!="admin":
            return redirect("home")
        arr = User.objects.exclude(designation="admin").exclude(designation="user").exclude(designation="merchant")
        for i in arr:
            i.status=get_from_tuple(User.STATUS, i.status)
        return render(request,"base/account.html",{'name' : request.user ,'arr':arr })

def delete_acc(request,UserID):
    if not (request.user.is_authenticated ):
        return render(request,"base/home.html",{})
    else:
        if request.user.designation!="admin":
            return redirect("home")
        arr=User.objects.filter(id=UserID)
        for i in arr:
            if i.status=="O":
                User.objects.filter(id=UserID).update(status="S")
            else:
                User.objects.filter(id=UserID).update(status="O")
        print(UserID)
        return redirect("iaccount_handling")

def add_acc(request):
    if not (request.user.is_authenticated ):
        return render(request,"base/home.html",{})
    else:
        if request.user.designation!="admin":
            return redirect("home")
        title = "Create an Employee"
        form = EmployeeRegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            if not user.acc_no:
                largest = User.objects.all().aggregate(
                    Max("acc_no")
                    )['acc_no__max']
                if largest:
                    user.acc_no = largest + 1
                else:
                    user.acc_no = 10000000
                x,y = user.regenerate_OTPseed()
                print(x)
            print("bc")
            user.designation="employee"
            user.save()
            email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
            user = authenticate(username=email, password=password)
            print(user)
            #return render(request,"base/loggedin.html",{'name':email, 'Acc':user.acc_no,'Pass':password})
            return redirect("iaccount_handling")
        context = {"title": title, "form": form}
        return render(request,"base/add_acc.html",context)


def modify_acc(request,UserID):
    if not (request.user.is_authenticated ):
        return render(request,"base/home.html",{})
    if request.user.designation!="admin":
        return redirect("home")
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
    if not (request.user.is_authenticated ):
        return render(request,"base/home.html",{})
    if request.user.designation!="employee" and request.user.designation!="manager":
        return redirect("home")
    print(txID)
    arr = TX_in.objects.filter(id=txID)
    for i in arr:
        if i.status!="3":
            return redirect("home")
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
    if not (request.user.is_authenticated ):
        return render(request,"base/home.html",{})
    if request.user.designation!="employee" and request.user.designation!="manager":
        return redirect("home")
    arr=TX_in.objects.filter(id=txID)
    for i in arr:
        if i.status!="3":
            return redirect("home")
    TX_in.objects.filter(id=txID).update(status="4")
    return redirect("ihome")

def approve_change_request(request,accNo):
    if not request.user.is_authenticated:
        return redirect("home")
    if request.user.designation!="admin":
        return redirect("home")
    arr=ModifiedUser.objects.filter(acc_no=accNo)
    for i in arr:
        if i.isModified!="1":
            return redirect("home")
    c=ModifiedUser.objects.filter(acc_no=accNo)[0]
    ModifiedUser.objects.filter(acc_no=accNo).update(isModified="2")
    User.objects.filter(acc_no=accNo).update(full_name=c.full_name,email=c.email,Address=c.Address,city=c.city,contact_no=c.contact_no)
    return redirect("userRequests")


def decline_change_request(request,accNo):
    if not request.user.is_authenticated:
        return redirect("home")
    if request.user.designation!="admin":
        return redirect("home")
    arr=ModifiedUser.objects.filter(acc_no=accNo)
    for i in arr:
        if i.isModified!="1":
            return redirect("home")
    ModifiedUser.objects.filter(acc_no=accNo).update(isModified="3")
    return redirect("userRequests")


def user_requests(request):
    if not request.user.is_authenticated:
        return redirect("home")
    if request.user.designation!="admin":
        return redirect("home")
    print("Inside ")
    changes=ModifiedUser.objects.filter(isModified="1")
    users=[]
    for i in changes:
        users.append(User.objects.filter(acc_no=i.acc_no)[0])
    return render(request,"base/modify_request_admin.html",{'changes':changes,'users':users})
    
    
                    
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

