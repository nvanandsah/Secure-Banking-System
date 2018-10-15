from django.conf.urls import url, include
from .views import transaction,trnsac
urlpatterns = [
	url(r'^$',transaction,name="transaction"),
	url(r'^transfer/',trnsac,name="transfer"),
]