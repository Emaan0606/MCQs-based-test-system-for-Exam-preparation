from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_page, name='signup'),
    path('login/', views.signin_page, name='login' ),
    path('signout/', views.signout_page, name='signout'),
    path('', views.main_dashboard, name='dashboard'),
    path('profile/', views.profile_page, name='profile'),
]
