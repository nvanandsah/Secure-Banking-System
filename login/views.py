from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from login.forms import modifyacc
from transaction.forms import trnsction
from .models import User
import pyotp
from transaction.models import TX_in
from django.db.models import Max
from django.contrib.auth import (authenticate,
                                 login,
                                 logout
                                 )
from Crypto.PublicKey import RSA

from base.models import ModifiedUser
def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Create a Bank Account"
        form = UserRegistrationForm(request.POST or None)
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
                key_pair = RSA.generate(1024)
                private_key = open(str(user.acc_no) + "privatekey.pem", "wb")
                private_key.write(key_pair.exportKey())
                private_key.close()
                public_key = open(str(user.acc_no) + "public_key.pem", "wb")
                Pubk = key_pair.publickey().exportKey()
                public_key.write(Pubk)
                public_key.close()
            #    key_pair = RSA.generate(1024)
            #    private_key = open("privatekey.pem", "w")
                print(x)
            print("bc")
            user.save()
            email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
            user = authenticate(username=email, password=password)
            print(user)
            #return render(request,"base/loggedin.html",{'name':email, 'Acc':user.acc_no,'Pass':password})
            if(user.designation == "user" or user.designation == "merchant" ):
                return render(request,"base/SignupSuccess.html",{'name' : user.email,'Acc':user.acc_no,'bal':user.balance, 'otp':y})
            else:
                return redirect("home")
        else:
            print(form.is_valid())
        context = {"title": title, "form": form}
        return render(request,"login/form.html",context)


def _login(request):
    if request.user.is_authenticated:
        print(request.user.designation)
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
            if(user.status=="O"):
                login(request, user)
            #messages.success(request, 'Welcome, {}!' .format(user.full_name))
                return redirect("home")
            else:
                context = {"form": form,
                   "title": title,
                   "message":"ur acc is suspended by admin",
                   }
                return render(request, "login/form.html", context)
        context = {"form": form,
                   "title": title
                   }
        return render(request, "login/form.html", context)


'''def Int_Login(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:   ''' 

def modify_acc(request):
    if not (request.user.is_authenticated ):
        return render(request,"base/home.html",{})
    if request.user.designation!="user" and request.user.designation!="merchant":
        return redirect("home")
    
    title = "Modify Account "
    Userlog=User.objects.filter(id=request.user.id)
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
        #print(UserID)
        #User.objects.filter(id=UserID).update(full_name=full_name,email=email,contact_no=contact_no,Address=Address,city=city)
        count=ModifiedUser.objects.filter(acc_no=request.user.acc_no).count()
        if count==0:
            userD=ModifiedUser(full_name=full_name,email=email,contact_no=contact_no,Address=Address,city=city,acc_no=request.user.acc_no,isModified="1")
            userD.save()
        else:
            ModifiedUser.objects.filter(acc_no=request.user.acc_no).update(full_name=full_name,email=email,contact_no=contact_no,Address=Address,city=city,acc_no=request.user.acc_no,isModified="1")
            
        return redirect("home")
    context = {"form": form,
                "title": title
                   }
    return render(request,"base/modify_acc.html",context)




def logout_view(request):  
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        logout(request)
        return redirect("home")

