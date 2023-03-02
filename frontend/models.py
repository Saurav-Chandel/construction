from django.db import models

# Create your models here.


class AboutUs(models.Model):
    title=models.CharField(max_length=100,null=True,blank=True)
    description=models.TextField()
    vedio_file=models.FileField(upload_to='about_video',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)