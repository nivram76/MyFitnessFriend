from django.urls import path
from . import views 

urlpatterns = [
    path('', views.foodcalc, name='foodcalc'),
    path('tdee', views.tdee, name='tdee'),
    path('room/<str:pk>/', views.room, name= 'room'),
    path('profile/<str:pk>/', views.userProfile, name= 'profile'),
    path('forums', views.forums, name= 'forums'),
    path('create-room', views.createRoom, name= 'create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name= 'update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name= 'delete-room'),
    path('login/', views.loginPage, name= 'login'),
    path('logout/', views.logoutUser, name= 'logout'),
    path('register/', views.registerUser, name= 'register'),
    path('delete-message/<str:pk>/', views.deleteMessage, name= 'delete-message'),



    
]