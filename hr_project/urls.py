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
    path('worker/<int:pk>/', hr_views.workerdetale, name='worker_detale'),
    path('company_worker/', hr_views.companylist, name='companylist'),
    path('company_departament/', hr_views.departamentlist, name='departamentlist'),
    path('departament_detale/<int:pk>/', hr_views.departamentdetale, name='departamentdetale'),
    path('position_detale/<int:pk>/', hr_views.positiondetale, name='positiondetale'),
    path('lay_off/<int:pk>/', hr_views.lay_off, name='lay_off'),
    path('put_on_hold/<int:pk>/', hr_views.put_on_hold, name='put_on_hold'),
    path('adddepartament/', hr_views.adddepartament, name='adddepartament'),
    path('addposition/', hr_views.AddPosition, name='addposition'),
    path('rolechoices/<int:pk>', hr_views.rolechoices, name='rolechoices'),
    path('profile/<int:pk>', hr_views.profile, name='profile'),
]
