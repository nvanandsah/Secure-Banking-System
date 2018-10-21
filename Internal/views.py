from django.shortcuts import render, redirect
from django.contrib import messages
from login.forms import UserRegistrationForm, UserLoginForm
from login.models import User
from django.db.models import Max
from django.contrib.auth import (authenticate,
                                 login,
                                 logout
                                 )
from django.shortcuts import render
from transaction.models import TX_in


# Create your views here.
def home(request):
	print(request.user.is_authenticated)
	#print(request.user.email)
	#print(request.user.acc_no)
	if not (request.user.is_authenticated):
		return render(request,"base/home.html",{})
	else:
		#arr = TX_in.objects.filter(acc_no=request.user.acc_no)
		arr = TX_in.objects.all()
		print(arr)
		return render(request,"base/loggedinEmployee.html",{'name' : request.user.email,'trns':arr})


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

