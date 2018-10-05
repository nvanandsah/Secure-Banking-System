from django.shortcuts import render

# Create your views here.
def home(request):
	print(request.user.is_authenticated)
	if not (request.user.is_authenticated):
		return render(request,"base/home.html",{})
	else:
		return render(request,"base/loggedin.html",{'content' : request.user})
