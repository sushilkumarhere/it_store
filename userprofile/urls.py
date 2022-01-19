from django.urls import path

from . import views

urlpatterns = [
    #path('aa/', views.index, name='index'),
    path('update/', views.ProfileView.as_view(), name='profile'),
    path('register_user/', views.register_user, name='register_user'),

]