from django.conf.urls import url, include
from .views import trnsac,add_money,debit_money,transactionMerch,approve_merch_req,decline_merch_req
urlpatterns = [
	url(r'^merchant_transaction/',transactionMerch,name="transactionMerch"),
	url(r'^transfer/',trnsac,name="transfer"),
	url(r'^addmoney/',add_money,name="addmoney"),
	url(r'^debitmoney/',debit_money,name="debitmoney"),
	url(r'^approve_Merch_Req/(?P<txID>[0-9]+)', approve_merch_req,
	    name='approveMReq'),
	url(r'^decline_Merch_Req/(?P<txID>[0-9]+)', decline_merch_req,
	    name='declineMReq'),

]