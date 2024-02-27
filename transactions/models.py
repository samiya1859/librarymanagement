from django.db import models
from user.models import UserLibraryAccount
from .constants import TRANSACTION_TYPE
from book.models import Book
from django.contrib.auth.models import User
# Create your models here.

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(UserLibraryAccount,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    amount = models.DecimalField(decimal_places=2 , max_digits=12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE,null=True,blank=True)
    balance_after_transaction = models.DecimalField(decimal_places=2 , max_digits=12,default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_returned = models.BooleanField(default=False,null=True,blank=True)
    
    class Meta:
        ordering = ['timestamp']
