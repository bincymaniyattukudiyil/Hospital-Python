from django.contrib.auth.models import User
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
    print(request.method)
    if request.method == 'POST':
        print('hi')
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
    print("here")
    print(request.method)
    if request.method == 'POST':
        print("here1")

        Username = request.POST['Username']
        Password = request.POST['Password']
        user = auth.authenticate(username=Username, password=Password)
        if user is not None:
            auth.login(request, user)
            userid = GetLoginId(request)

            items = Registration.objects.filter(id=userid)
            print(items)
            return render(request, "Home.html", {'items': items, 'username': Username})

        else:
            return render(request, 'Index.html')
    return render(request,"Login.html")
def logout(request):
    auth.logout(request)
    return render(request,"Index.html")