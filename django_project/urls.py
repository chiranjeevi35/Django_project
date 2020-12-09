"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from credicxo import views

urlpatterns = [
    path('admin/', admin.site.urls),
 #   path('akshay', views.fun),
  #  path('adduser',views.addstudent),
   # path('user',views.getuser),
    path('signup',views.signup_view),
    path('login',views.login_view),
    path('forget',views.forget_view),
    path('validate',views.validate_token),
    path('addteacher',views.addteacher_view),
    path('getallusers',views.getallusers_view),
    path('listteacher',views.listteacher_view),
    path('addstudentbyteacher',views.addstudentby_teacher),
    path('liststudent',views.liststudent_view),
    path('getindividualdetails',views.getindividualdetails),

]
