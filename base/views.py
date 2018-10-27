from django.shortcuts import render,redirect
from transaction.models import TX_in
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
		if request.user.designation=="employee":
			return redirect("ihome")
		arr = TX_in.objects.filter(fromUser_id=request.user.id)
		print(arr)
		print(request.user.id)
		for i in arr:
			i.status=get_from_tuple(TX_in.STATUS, i.status)
#		return render(request,"base/SignupSuccess.html",{'name' : request.user.email,'Acc':request.user.acc_no,'bal':request.user.balance, 'trns':arr, 'otp':request.user.OTPSeed})
#def loggedinPage(request):
		return render(request,"base/loggedin.html",{'name' : request.user.email,'Acc':request.user.acc_no,'bal':request.user.balance, 'trns':arr})
