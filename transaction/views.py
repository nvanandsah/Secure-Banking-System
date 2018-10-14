from django.shortcuts import render

# Create your views here.
def transaction(request):
	if not (request.user.is_authenticated):
		return render(request,"base/home.html",{})
	else:
		return render(request,"transaction/tr_page.html",{'name' : request.user.full_name,'Acc':request.user.acc_no,'bal':request.user.balance})