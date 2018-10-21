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
		arr = TX_in.objects.filter(fromUser_id=request.user.id)
		print(arr)
		print(request.user.id)
		return render(request,"base/loggedin.html",{'name' : request.user.email,'Acc':request.user.acc_no,'bal':request.user.balance, 'trns':arr})
