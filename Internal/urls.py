from django.conf.urls import url, include
from .views import home,_login,signup,logout
urlpatterns = [
	url(r'^$',home,name="ihome"),
	url(r'^login/',_login,name="ilogin"),
	url(r'^signup/',signup,name="isignup"),
	url(r'^logout/',logout,name="ilogout"),
]