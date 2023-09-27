from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('rooms/<str:pk>/', views.room, name='room'),
    path('room/create-room/', views.create_room,name="create-room"),
    path('room/update-room/<str:pk>/', views.upadate_room,name="update-room"),
    path('room/delete-room/<str:pk>/', views.delete_room,name="delete-room"),
    path('room/delete-message/<str:pk>/', views.delete_message,name="delete-message"),
    path('profile/<str:pk>/', views.userProfile,name="user-profile"),
    path('update-user/', views.updateUser,name="update-user"),
    path('topics/', views.topicsPage,name="topics"),
    path('activity/', views.activitiesPage,name="activity"),



]