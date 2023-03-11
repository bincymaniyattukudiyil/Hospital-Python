from django.urls import path

from Accounts import views

urlpatterns = [
    path('',views.index,name='index'),
    path('Login/', views.Login, name='Login'),
    path('Register/', views.Register, name='Register'),
    path('logout/', views.logout, name='logout')
]