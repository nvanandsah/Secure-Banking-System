from django.conf.urls import url, include
from .views import transaction,transac
urlpatterns = [
	url(r'^$',transaction,name="transaction"),
	url(r'^transfer/',transac,name="transfer"),
]