from django.db import models

# from rest.models import MyUser
# Create your models here.
from rest.models import MyUser


class Post(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=200,default='')
    description=models.CharField(max_length=555,default='')
    created_post=models.DateField(null=True)

    def __str__(self):
        return self.title+ ' '+str(self.created_post)

class Comment(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    comment=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.comment