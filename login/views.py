from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import User
from django.db.models import Max
from django.contrib.auth import (authenticate,
                                 login,
                                 logout
                                 )
# Create your views here.
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
                # gets the largest account number
                largest = User.objects.all().aggregate(
                    Max("acc_no")
                    )['acc_no__max']
                if largest:
                    # creates new account number
                    user.acc_no = largest + 1
                else:
                    # if there is no other user, sets users account number to 10000000.
                    user.acc_no = 10000000
            print("bc")
            user.save()
            email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
            user = authenticate(username=email, password=password)
            print(user)
            return render(request,"base/loggedin.html",{'name':email})
        else:
            print(form.is_valid())
        context = {"title": title, "form": form}
        return render(request,"")


def home(request):
    if request.user.is_authenticated:      
        return render(request, "login/home.html", context) 
