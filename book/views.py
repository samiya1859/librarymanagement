from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from .forms import BookForm,ReviewForm
from .models import Book,Review,Borrow
from transactions.models import Transaction
from category.models import Category
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView,TemplateView
from django.views import View
from django.views.generic import FormView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

# class BookDetailView(DetailView):
#     model = Book
#     template_name = 'book_detail.html'
#     form_class = ReviewForm
#     context_object_name = 'book'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         book = self.get_object()

#         # Check if the book is borrowed
#         is_borrowed = book.is_borrowed
        
#         # Pass the flag to the context
#         context['is_borrowed'] = is_borrowed

#         # Initialize the form for the current user
#         context['form'] = ReviewForm(user=self.request.user)

#         return context
@method_decorator(csrf_protect, name='dispatch')    
class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    form_class = ReviewForm
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()

        # Check if the book is borrowed
        is_borrowed = book.is_borrowed
        
        # Pass the flag to the context
        context['is_borrowed'] = is_borrowed

        # Initialize the form for the current user
        

        return context
    

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            # Save the review
            review = review_form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_details', pk=book.pk)
        else:
            # If the form is invalid, re-render the template with the form and existing reviews
            return self.render_to_response(self.get_context_data())

def AllbookView(request, cat_slug=None):
    data = Book.objects.all()
    categories = Category.objects.all()
    category = None
    

    if cat_slug:
        category = get_object_or_404(Category, slug=cat_slug)
        data = Book.objects.filter(category=category)

    return render(request, 'allbooks.html', {'data': data, 'category': category, 'categories': categories})

@login_required
def borrow_history(request):
    
    borrowed_books = Borrow.objects.filter(user = request.user)
    
    return render(request, 'borrowhis.html', {'borrowed_books': borrowed_books})

class AddReview(FormView):
    template_name = 'book_detail.html'
    form_class = ReviewForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        book_id = self.kwargs['book_id']
        book = Book.objects.get(id=book_id)
        kwargs['instance'] = book
        return kwargs

    def form_valid(self, form):
        book_id = self.kwargs['book_id']
        book = Book.objects.get(id=book_id)
        review = form.save(commit=False)
        review.book = book
        review.save()
        messages.success(self.request, 'Review added successfully!')
        return redirect('book_details', id=book_id)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to add review. Please check the form.')
        return super().form_invalid(form)
    




@method_decorator(csrf_protect, name='dispatch')
class Comment_views(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'book_detail.html'
 
    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        book = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.user = request.user
            new_review.save()
        return self.get(request, *args, **kwargs)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()
        
        borrows = Borrow.objects.filter(user=self.request.user, book=book)
        
        if borrows:
            review_form = ReviewForm()
            context['review_form'] = review_form

        context['reviews'] = reviews
        context['book'] = book
        return context