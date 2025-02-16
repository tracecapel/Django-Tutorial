from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    
    
    path('',views.home, name="home"),
    path('room/<int:pk>/', views.room, name="room"),

    path('create-room/', views.createRoom, name="create-room"),

    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),

    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
]