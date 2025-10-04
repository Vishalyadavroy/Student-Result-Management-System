"""
URL configuration for studentResultManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from resultapp.views import index ,admin_login ,admin_dashboard ,create_class

urlpatterns = [
    path('Vishaladmin/', admin.site.urls),
    path('' ,index, name='index'),
    path('admin-login' ,admin_login, name='admin-login'),
    path('admin_dashboard' ,admin_dashboard, name='admin_dashboard'),
    path('creat_class/' ,create_class, name='create_class'),
]
