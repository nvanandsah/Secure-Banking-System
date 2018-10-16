from django.conf.urls import url, include
from .views import transaction,trnsac,add_money
urlpatterns = [
	url(r'^$',transaction,name="transaction"),
	url(r'^transfer/',trnsac,name="transfer"),
	url(r'^addmoney/',add_money,name="addmoney"),

]