from django.urls import path
from . import views 

urlpatterns = [
    path('', views.foodcalc, name='foodcalc'),
    path('tdee', views.tdee, name='tdee'),
]