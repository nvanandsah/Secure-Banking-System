from django.conf.urls import url, include
from .views import home,_login,signup,logout
from Internal.views import approve_transaction,decline_transaction
urlpatterns = [
	url(r'^$',home,name="ihome"),
	url(r'^login/',_login,name="ilogin"),
	url(r'^signup/',signup,name="isignup"),
	url(r'^logout/',logout,name="ilogout"),
	url(r'^approve_tx/(?P<txID>[0-9]+)', approve_transaction,
	    name='approve_tx_id'),
	url(r'^decline_tx/(?P<txID>[0-9]+)', decline_transaction,
	    name='decline_tx_id'),
]