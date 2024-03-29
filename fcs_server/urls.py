"""fcs_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from login.views import signup, _login, logout_view,modify_acc
from base.views import home,homeMerchant,user_details

urlpatterns = [
    url(r'^login/',_login,name="login"),
    url(r'^logout/',logout_view,name="logout"),
    url(r'^signup/',signup,name="signup"),
    url(r'^transaction/',include('transaction.urls')),
    url(r'^internal/',include('Internal.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$',home,name="home"),
    url(r'^home_merchant',homeMerchant,name="homeMerchant"),
    url(r'^modify_acc/', modify_acc,
        name='modify_acc'),
    url(r'^user_details',user_details,name="user_details"),

    
]
