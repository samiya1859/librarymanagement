from django.db.models.query import QuerySet
from book.models import Book
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import TransactionForm,DepositForm
from .models import Transaction
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView,ListView
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from .constants import DEPOSIT,RETURN,BORROW
from django.db.models import Sum
from book.models import Borrow
# Create your views here.


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # template e context data pass kora
        context.update({
            'title': self.title
        })

        return context
    
@method_decorator(csrf_protect, name='dispatch')    
class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit Money'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(update_fields=['balance'])
        
        # Create a new transaction object and set the user field
        transaction = Transaction.objects.create(
            user=self.request.user,  # Set the user field
            account=account,
            amount=amount,
            transaction_type=DEPOSIT,
            timestamp=timezone.now(),
            book=None,
        )
        
        # Send email notification
        mail_subject = "Deposit message"
        message = render_to_string('deposit_email.html', {
            'user': self.request.user,
            'amount': amount,
        })
        to_email = self.request.user.email
        send_email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
        
        messages.success(self.request, f'{"{:,.2f}".format(float(amount))}$ was deposited successfully!')
        return redirect('home')
    
# class BorrowBookView(LoginRequiredMixin, View):
#     def get(self, request, id):
#         book = get_object_or_404(Book, id=id)
#         user = request.user
#         account = user.account
#         borrowing_price = book.borrowing_price

#         if account.balance < borrowing_price:
#             messages.error(request, "Insufficient balance to borrow this book")
#             return render(request, 'book_detail.html')

#         balance_after_transaction = account.balance - borrowing_price

#         transaction = Transaction.objects.create(
#             user=user,
#             account=account,
#             book=book,
#             amount=borrowing_price,
#             transaction_type=BORROW,
#             balance_after_transaction=balance_after_transaction,
#         )
#         borrow = Borrow.objects.create(
#             user=user,
#             book=book,
           
#         )
#         print(borrow)
#         account.balance -= borrowing_price
#         account.save()

#         messages.success(request, f"You have successfully borrowed '{book.title}'.")
        
#         # Redirect the user to a specific URL after a successful borrowing
#         return redirect('book_details', pk=id)     
    
class BorrowBookView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        user = request.user
        account = user.account
        borrowing_price = book.borrowing_price

        if account.balance < borrowing_price:
            messages.error(request, "Insufficient balance to borrow this book")
            return render(request, 'book_detail.html')

        balance_after_transaction = account.balance - borrowing_price

        transaction = Transaction.objects.create(
            user=user,
            account=account,
            book=book,
            amount=borrowing_price,
            transaction_type=BORROW,
            balance_after_transaction=balance_after_transaction,
        )
        borrow = Borrow.objects.create(
            user=user,
            book=book,
        )
        print(borrow)

        # Update the is_borrowed field to True
        book.is_borrowed = True
        book.save()

        account.balance -= borrowing_price
        account.save()
        
        mail_subject = "Borrowing Message"
        message = render_to_string('borrow_email.html', {
            'user': self.request.user,
            'amount': borrowing_price,
        })
        to_email = self.request.user.email
        send_email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
        messages.success(request, f"You have successfully borrowed '{book.title}'.")

        # Redirect the user to a specific URL after a successful borrowing
        return redirect('book_details', pk=id)

# class ReturnBookView(LoginRequiredMixin, View):
#     def get(self, request, transaction_id):
#         transaction = get_object_or_404(Transaction, id=transaction_id) 
#         user = request.user
        
#         if transaction.user != user:
#             messages.error(request, "You are not eligible to return this book")
#             return render(request, 'book_detail.html')
        
#         # Mark the transaction as returned
#         transaction.is_returned = True
#         transaction.save()
        
#         # Increase the user's balance by the borrowing price of the book
#         user.account.balance += transaction.book.borrowing_price
#         user.account.save()

#         messages.success(request, f"You have successfully returned '{transaction.book.title}'.")
#         return redirect('report', id=transaction_id)
    
# class ReturnBookView(LoginRequiredMixin, View):
#     def get(self, request, transaction_id):
#         transaction = get_object_or_404(Transaction, id=transaction_id) 
#         user = request.user
        
#         if transaction.user != user:
#             messages.error(request, "You are not eligible to return this book")
#             return render(request, 'book_detail.html')
        
        
#         transaction.is_returned = True
#         transaction.save()
        
#         if transaction.book:
#             # Increase the user's balance by the borrowing price of the book
#             user.account.balance += transaction.book.borrowing_price
#             user.account.save()
#             messages.success(request, f"You have successfully returned '{transaction.book.title}'.")
#         else:
#             messages.error(request, "The transaction does not have an associated book.")
        
#         return redirect('report', transaction_id=transaction_id)
def send_return_email(user,amount,subject,template):
    message = render_to_string(template,{
        'user':user,
        'amount':amount,
        
    })
    send_email = EmailMultiAlternatives(subject,'',to=[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()
    
class ReturnBookView(LoginRequiredMixin, View):
    def get(self, request, transaction_id):
        # Retrieve the transaction object
        transaction = get_object_or_404(Transaction, id=transaction_id)
        
        # Check if the transaction is already returned
        if transaction.is_returned:
            messages.warning(request, "This book has already been returned.")
            return redirect('report')  # Redirect to some view
            
        # Mark the transaction as returned
        transaction.is_returned = True
        transaction.save()
        
        # Update the user's account balance
        user = request.user
        account = user.account
        if transaction.book:
            account.balance += transaction.amount  # Update user's account balance
            account.save()
            
            # Display success message
            messages.success(request, f"You have successfully returned '{transaction.book.title}'.")
        else:
            # If the transaction doesn't have an associated book
            messages.error(request, "The transaction does not have an associated book.")
        
        # Call send_return_email function with required arguments
        subject = "Book Return Confirmation"
        template = "return_email.html"
        send_return_email(user, transaction.amount, subject, template)
        
        return redirect('report')

    
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transaction_report.html'
    model = Transaction

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%y-%m-%d').date()

            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['account'] = self.request.user.account
        return context
