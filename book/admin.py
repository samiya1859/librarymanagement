from django.contrib import admin
from .models import Book,Borrow,Review,Author
# Register your models here.
admin.site.register(Book)
admin.site.register(Borrow)
admin.site.register(Review) 
admin.site.register(Author) 

