from django.conf.urls import url, include
from .views import transaction,trnsac,add_money,debit_money
urlpatterns = [
	url(r'^$',transaction,name="transaction"),
	url(r'^transfer/',trnsac,name="transfer"),
	url(r'^addmoney/',add_money,name="addmoney"),
	url(r'^debitmoney/',debit_money,name="debitmoney"),

]