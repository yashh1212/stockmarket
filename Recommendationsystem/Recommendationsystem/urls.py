"""Recommendationsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import index
from . import UserDashboard
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index',index.page1),
    path('register',index.register),
    path('login',index.login),
    path('userlogin',index.userlogin),
    path('userhome',UserDashboard.userhome),
    path('getstock',UserDashboard.getstock),
    path('stockpred',UserDashboard.stockpred),
    path('predict',UserDashboard.predict),
    path('addwatchlist',UserDashboard.addwatchlist),
    path('livestock',UserDashboard.livestock),
    path('dateprediction',UserDashboard.dateprediction),
    path('mysearches',UserDashboard.mysearches),
    path('mywatchlist',UserDashboard.mywatchlist),
    path('getcurrentstock',UserDashboard.getcurrentstock),
    path('logout',UserDashboard.logout),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
