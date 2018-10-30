from django.shortcuts import render,redirect
from transaction.models import TX_in
from .models import ModifiedUser
# Create your views here.

def get_from_tuple(my_tuple, key):
    try:
        return next(y for x, y in my_tuple if x == key)
    except StopIteration:
        return None

def home(request):
	print(request.user.is_authenticated)
	#print(request.user.email)
	#print(request.user.acc_no)
	if not (request.user.is_authenticated):
		return render(request,"base/home.html",{})
	else:
		#arr = TX_in.objects.filter(acc_no=request.user.acc_no)
		if request.user.designation!="user":
			return redirect("ihome")
		arr = TX_in.objects.filter(fromUser_id=request.user.id)
		CHOICE = (
    		("1", "Debit"),
    		("2", "Credit"),
			("3", "Transfer"),
    	)
		STATUS = (
            ('0', "Nothing"),
            ('1', "Initiated"),
            ('2', "Approved"),
            ('3', "Declined"),
        )
		print(arr)
		print(request.user.id)
		for i in arr:
			i.status=get_from_tuple(TX_in.STATUS, i.status)
			i.Tr_type=get_from_tuple(CHOICE, i.Tr_type)
		changes=ModifiedUser.objects.filter(acc_no=request.user.acc_no)
		for i in changes:
			i.isModified=get_from_tuple(STATUS, i.isModified)
#		return render(request,"base/SignupSuccess.html",{'name' : request.user.email,'Acc':request.user.acc_no,'bal':request.user.balance, 'trns':arr, 'otp':request.user.OTPSeed})
#def loggedinPage(request):
		return render(request,"base/loggedin.html",{'name' : request.user.email,'Acc':request.user.acc_no,'bal':request.user.balance, 'trns':arr,'changes':changes})
