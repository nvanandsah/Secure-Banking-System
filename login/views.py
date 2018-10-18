from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from transaction.forms import trnsction
from .models import User
from django.db.models import Max
from django.contrib.auth import (authenticate,
                                 login,
                                 logout
                                 )

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
            print("bc")
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


def Int_Login(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:    




def logout_view(request):  
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        logout(request)
        return redirect("home")

