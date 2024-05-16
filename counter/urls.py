from django.urls import path
from . import views 

urlpatterns = [
    path('', views.foodcalc, name='foodcalc'),
    path('tdee', views.tdee, name='tdee'),
    path('room/<str:pk>/', views.room, name= 'room'),
    path('forums', views.forums, name= 'forums')
]