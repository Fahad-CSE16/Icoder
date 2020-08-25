
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=40)
    slug = models.CharField(max_length=40)
    content = models.TextField()
    views=models.IntegerField(default=0)
    timeStamp=models.DateTimeField(blank= True)
    thumbnail = models.ImageField(upload_to='blog/images', default="")

    def __str__(self):
        return self.title+ ' by: '+ self.author

class BlogComment(models.Model):
    sno=models.AutoField(primary_key = True)
    comment=models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post =  models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null= True)
    timestamp=models.DateTimeField(default= now)

    def __str__(self):
        return self.user.username + ": " +self.comment[0:13] 
    


