"""hr_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from hrapp import views as hr_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hr_views.home, name='home'),
    path('signup_company/', hr_views.signup_company, name='signup_company'),
    path('signup_worker/', hr_views.signup_worker, name='signup_worker'),
    path('sign_in/', hr_views.sign_in, name='signin'),
    path('sign_out/', hr_views.sign_out, name='sign_out'),
    path('free_worker/', hr_views.freelist, name='free_worker'),
]
