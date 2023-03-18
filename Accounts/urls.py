from django.urls import path

from Accounts import views

urlpatterns = [
    path('',views.index,name='index'),


    path('Login/', views.Login, name='Login'),
    path('Register/', views.Register, name='Register'),
    path('PostBlog/', views.PostBlog, name='PostBlog'),
    path('ViewBlog/', views.ViewBlog, name='ViewBlog'),
    path('BlogDetail/<int:id>', views.BlogDetail, name='BlogDetail'),
    path('EditBlog/<int:id>', views.EditBlog, name='EditBlog'),
    path('ViewMyBlog/', views.ViewMyBlog, name='ViewMyBlog'),
    path('Draft/', views.Draft, name='Draft'),
    path('MyBlogDetail/<int:id>', views.MyBlogDetail, name='MyBlogDetail'),
    path('DoctorsList/', views.DoctorsList.as_view(), name='DoctorsList'),
    path('BookAppoinment/<int:id>', views.BookAppoinment, name='BookAppoinment'),

    path('logout/', views.logout, name='logout'),


]