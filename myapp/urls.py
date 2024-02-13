from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('video/', views.video, name='video'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('list/', views.list, name = 'list'),
    path('delete-room/<str:room_name>/', views.delete_room, name='delete-room'),
]
