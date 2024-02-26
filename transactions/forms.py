from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount'
        ]

    def __init__(self,*args,**kwargs):
        self.account = kwargs.pop('account',None)
        super().__init__(*args,**kwargs)

    def save(self,commit=True):
        if self.account:
            self.instance.account = self.account
            self.instance.balance_after_transaction = self.account.balance
        return super().save(commit=commit)
    

class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(f'You must deposit at least {min_deposit_amount}$')
        return amount

    