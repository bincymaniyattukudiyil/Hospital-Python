from django.contrib.auth.models import User
from django.http import HttpResponse
from django.forms import forms
from django.shortcuts import render,redirect
from django.contrib import messages, auth
from . models import *

# Create your views here.
def GetLoginId(request):

    current_user = request.user
    name = current_user.username
    objs = Registration.objects.filter(Username=name)
    if len(objs) == 1:
        obj = objs[0]
    else:
        pass
    userid = obj.id
    return userid

def index(request):
    return render(request, "Index.html")
def Register(request):
    if request.method == 'POST':
        FirstName = request.POST['FirstName']
        LastName = request.POST['LastName']
        ProfileImg = request.FILES['ProfileImg']
        EmailId = request.POST['EmailId']
        PhoneNumber = request.POST['PhoneNumber']
        Address = request.POST['Address']
        Type = request.POST['Type']
        Username = request.POST['Username']
        Password = request.POST['Password']
        ConfirmPassword=request.POST['ConfirmPassword']
        if(ConfirmPassword !=Password):
            messages.info(request, "Pasformssword Miss Match...")
            return redirect('Register')
            # return render(request, 'Register.html', {'messages': messages})
        else:
            if Registration.objects.filter(Username=Username).exists():
               messages.info(request, "username exist")
               return redirect('Register')

            else:
             Profile = Registration(FirstName=FirstName, LastName=LastName,
                                         ProfileImg=ProfileImg, EmailId=EmailId,
                                         PhoneNumber=PhoneNumber,
                                         Address=Address, Type=Type,
                                         Username=Username, Password=Password)
            Profile.save()
            user = User.objects.create_user(password=Password,
                                            username=Username)
            user.save()
            messages.info(request, "successfully registered....")
            return redirect('Register')
    return render(request,"Register.html")
def Login(request):
    print(request.method)
    if request.method == 'POST':

        Username = request.POST['Username']
        Password = request.POST['Password']
        user = auth.authenticate(username=Username, password=Password)
        if user is not None:
            auth.login(request, user)
            userid = GetLoginId(request)

            items = Registration.objects.filter(id=userid)

            if items[0].Type =='Doctor':
                return render(request, "Home.html", {'items': items, 'username': Username})
            else:
                return render(request, "PatientHome.html", {'items': items, 'username': Username})

        else:
            return render(request, 'Index.html')
    return render(request,"Login.html")
def logout(request):
    auth.logout(request)
    return render(request,"Index.html")
def PostBlog(request):

    items = BlogCategory.objects.all()
    if request.method=='POST':
        BlogTitle = request.POST['BlogTitle']
        BlogCategoryID = request.POST['BlogCategoryID']
        BlogImg = request.FILES['BlogImg']
        BlogContent = request.POST['BlogContent']
        BlogSummery = request.POST['BlogSummery']
        print(BlogImg)
        value = request.POST['PostBlog']
        if value=='Draft':
            BlogStatus=2
        else:
            BlogStatus=1
        RegistrationID=GetLoginId(request)
        print(BlogStatus)
        BlogPost = Blog(BlogTitle=BlogTitle, BlogCategoryID=BlogCategoryID,
                               BlogImg=BlogImg, BlogContent=BlogContent,
                               BlogSummery=BlogSummery,
                               BlogStatus=BlogStatus, RegistrationID=RegistrationID)
        BlogPost.save()
        if BlogStatus==1:
            return HttpResponse("<html><body>Blog Posted Susscessfully....<a href=" '/PostBlog' ">Home</a></body></html>")
            # messages.info(request, "Blog Posted Susscessfully....")
        else:
            return HttpResponse("<html><body>blog has been saved....<a href=" '/PostBlog' ">Home</a></body></html>")
            # messages.info(request, "blog has been saved....")
        return render(request, 'PostBlog.html',{'items':items})

    return render(request, 'PostBlog.html',{'items':items})
def ViewBlog(request):
    item = BlogCategory.objects.all()
    if request.method == 'POST':
        BlogCategoryID=request.POST['BlogCategoryID']
        print(BlogCategoryID)
        items = Blog.objects.filter(BlogCategoryID=BlogCategoryID,BlogStatus=1)
        return render(request, 'ViewBlog.html', {'items': items, 'item': item})
    items = Blog.objects.filter(BlogStatus=1)
    return render(request, 'ViewBlog.html', {'items': items,'item':item})
def BlogDetail(request,id):
    item = BlogCategory.objects.all()
    items = Blog.objects.filter(id=id)
    return render(request, 'BlogDetail.html', {'items': items, 'item': item})
def Draft(request):

    userid = GetLoginId(request)
    items = Blog.objects.filter(BlogStatus=2,RegistrationID=userid)

    return render(request, 'DraftBlogs.html', {'items': items})
def EditBlog(request,id):

    item = BlogCategory.objects.all()

    if request.method == 'POST':
        print('here i am')

        BlogTitle = request.POST['BlogTitle']
        BlogCategoryID = request.POST['BlogCategoryID']
        BlogImg = request.FILES['BlogImg']
        BlogContent = request.POST['BlogContent']
        BlogSummery = request.POST['BlogSummery']
        userid=GetLoginId(request)

        print(BlogImg)
        value = request.POST['EditBlog']
        if value == 'Draft':
            BlogStatus = 2
        else:
            BlogStatus = 1

        Newitems = Blog.objects.filter(id=id).update(
        BlogTitle = BlogTitle,
        BlogCategoryID = BlogCategoryID,
        BlogContent = BlogContent,
        BlogSummery = BlogSummery,
        RegistrationID = userid,
        BlogStatus=BlogStatus
        )

        if BlogStatus==1:
            return HttpResponse("<html><body>Blog Posted Susscessfully....<a href=" '/Draft' ">Home</a></body></html>")
            # messages.info(request, "Blog Posted Susscessfully....")
        else:
            return HttpResponse("<html><body>blog has been saved........<a href=" '/Draft' ">Home</a></body></html>")
            # messages.info(request, "blog has been saved....")
        items = Blog.objects.filter(BlogStatus=2, RegistrationID=userid)
        return render(request, 'DraftBlogs.html',{'items': items})
    items = Blog.objects.filter(id=id)
    return render(request, 'EditBlog.html', {'items': items, 'item': item})

def ViewMyBlog(request):
    item = BlogCategory.objects.all()
    userid = GetLoginId(request)
    if request.method == 'POST':
        BlogCategoryID = request.POST['BlogCategoryID']
        userid = GetLoginId(request)
        print(BlogCategoryID)
        items = Blog.objects.filter(BlogCategoryID=BlogCategoryID,RegistrationID=userid)
        return render(request, 'ViewMyBlog.html', {'items': items, 'item': item})
    items = Blog.objects.filter(RegistrationID=userid)
    return render(request, 'ViewMyBlog.html', {'items': items, 'item': item})

def MyBlogDetail(request,id):
    item = BlogCategory.objects.all()
    items = Blog.objects.filter(id=id)
    return render(request, 'MyBlogDetail.html', {'items': items, 'item': item})