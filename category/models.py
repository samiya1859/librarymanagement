from django.db import models

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20,unique=True,null=True,blank=True)

    def __str__(self):
        return self.category