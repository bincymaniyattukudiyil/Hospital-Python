from django.db import models

# Create your models here.
class Registration(models.Model):
    FirstName=models.CharField(max_length=50)
    LastName=models.CharField(max_length=50)
    ProfileImg=models.ImageField(upload_to='Images')
    EmailId=models.CharField(max_length=50)
    PhoneNumber=models.IntegerField()
    Address=models.TextField(max_length=50)
    Type=models.CharField(max_length=50)
    Username=models.TextField(max_length=20,unique=True)
    Password = models.TextField(max_length=20)