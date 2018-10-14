from django.conf.urls import url, include
from .views import transaction
urlpatterns = [
	url(r'^$',transaction,name="transaction")
]