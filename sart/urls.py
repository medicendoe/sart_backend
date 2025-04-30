"""
URL configuration for sart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from .views import SampleCreate, DummyGetLast, CenterCreate, CenterList, PersonnelCreate, PersonnelList, PatientCreate, PatientList, PersonnelLogin, PersonnelByCenter, PatientsByPersonnel, DeviceCreate

urlpatterns = [
    path('sample/create/', SampleCreate.as_view()),
    path('sample/dummy/last/', DummyGetLast.as_view()),
    path('center/create/', CenterCreate.as_view()),
    path('center/getall/', CenterList.as_view()),
    path('personnel/create/', PersonnelCreate.as_view()),
    path('personnel/getall/', PersonnelList.as_view()),
    path('personnel/login/', PersonnelLogin.as_view()),
    path('patient/create/', PatientCreate.as_view()),
    path('patient/getall/', PatientList.as_view()),
    path('device/create/', DeviceCreate.as_view()),
    path('personnel/center/<int:center_id>/', PersonnelByCenter.as_view(), name='personnel-by-center'),
    path('patient/personnel/<int:personnel_id>/', PatientsByPersonnel.as_view(), name='patients-by-personnel'),
]
