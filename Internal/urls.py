from django.conf.urls import url, include
from .views import home,_login,signup,logout
from Internal.views import approve_transaction,decline_transaction,account_handling,delete_acc,add_acc,modify_acc,user_requests,approve_change_request,decline_change_request
urlpatterns = [
	url(r'^$',home,name="ihome"),
	url(r'^login/',_login,name="ilogin"),
	url(r'^signup/',signup,name="isignup"),
	url(r'^logout/',logout,name="ilogout"),
	url(r'^approve_tx/(?P<txID>[0-9]+)', approve_transaction,
	    name='approve_tx_id'),
	url(r'^decline_tx/(?P<txID>[0-9]+)', decline_transaction,
	    name='decline_tx_id'),
	url(r'^account/',account_handling,name="iaccount_handling"),
	url(r'^user_requests/',user_requests,name="userRequests"),
	url(r'^decline_acc/(?P<UserID>[0-9]+)', delete_acc,
	    name='delete_acc'),
	url(r'^add_acc/', add_acc,
	    name='add_acc'),
	url(r'^modify_acc/(?P<UserID>[0-9]+)', modify_acc,
        name='modify_acc'),
	url(r'^approve_change_request/(?P<accNo>[0-9]+)', approve_change_request,
        name='approveChangeRequest'),
	url(r'^decline_change_request/(?P<accNo>[0-9]+)', decline_change_request,
        name='declineChangeRequest'),
		
]