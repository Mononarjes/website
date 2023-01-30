from django.db import models
from ckeditor.fields import RichTextField
from django.db.models import CASCADE
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views_number = models.IntegerField(default=0)
    promoted = models.BooleanField(default=False)
    post_body = RichTextField(blank = True, null=True)
    image = models.ImageField(blank = True, null=True, upload_to= 'storage/')
    title = models.CharField(max_length=250)
    date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.title}"
    
    def get_absolute_url(self):
        return reverse("userpanel")
    
    

class comment(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE, related_name='comments')
    comment_body = models.TextField()
    author = models.CharField(max_length=40)
    date = models.DateTimeField()
    root = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='theroot')
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return '%s -- %s' %(self.post.title, self.author)
    
    def get_absolute_url(self):
        return reverse("userpanel")
