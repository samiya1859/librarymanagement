from django.db import models
from django.contrib.auth.models import User
from category.models import Category

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=30,null=True,blank=True)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    Author = models.ForeignKey(Author,on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='book/media/book_images/')
    borrowing_price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    is_borrowed = models.BooleanField(default=False,null=True)
    @property
    def reviews(self):
        return self.review_set.all()

    def __str__(self) :
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='reviews')
    name = models.CharField(max_length=20)
    review = models.TextField()
    reviewDate = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Reviewd by {self.name}"

class Borrow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='borrows')
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='borrows')
    
    
    
    

