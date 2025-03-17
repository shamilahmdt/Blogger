from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=225)    

class Tag(models.Model):
    name = models.CharField(max_length=225)

class Blog(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    date = models.DateField(auto_now=True)
    image =models.ImageField(upload_to='blogimg')
    description_big = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
