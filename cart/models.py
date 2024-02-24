from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# from django_resized import ResizedImageField 
from cloudinary.models import CloudinaryField
# check tis comments
class projects(models.Model):
    pname=models.CharField(max_length=25)
    desc=models.TextField()
    domain=models.CharField(max_length=10)
    stack=models.CharField(max_length=60)
    link=models.URLField(null=True)
    # image=ResizedImageField(size=[600,600],quality=85,upload_to="proj_imgs",null=True)
    image = CloudinaryField('image', folder='proj_imgs', blank=True, null=True)
    info=models.TextField()
    stud=models.CharField(max_length=25)
    date=models.DateField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name='project_like')

    
    def number_of_likes(self):
        return self.likes.count()
  

    def __str__(self):
        return str(self.pname)
# Create your models here.

class full_user(models.Model):
    s=models.CharField(max_length=25)
    # s=models.ForeignKey(User,on_delete=models.CASCADE,null=True) 
    college=models.CharField(max_length=60,null=True)
    sem=models.CharField(max_length=10,null=True)
    # photo=ResizedImageField(size=[600,600],quality=85,upload_to="user_imgs",null=True)
    photo = CloudinaryField('image', folder='user_imgs', blank=True, null=True)
    bio=models.CharField(max_length=120,null=True)
    github=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.s

class comments(models.Model):
    comment=models.TextField()
    user=models.ForeignKey(full_user,on_delete=models.CASCADE)       
    post=models.ForeignKey(projects,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    time=models.DateTimeField(default=now)
    def __str__(self):
        return self.comment +"... by "+self.user.s     