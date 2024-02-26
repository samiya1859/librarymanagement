from django.urls import path
from .views import AllbookView, BookDetailView,borrow_history,Comment_views
from transactions.views import BorrowBookView

urlpatterns = [
   path('allbooks/', AllbookView, name='allbooks'), 
   path('category/<slug:cat_slug>/', AllbookView, name='category_wise_book'),
   path('details/<int:id>/', Comment_views.as_view(), name='book_details'),
   path('borrow/<int:id>/',BorrowBookView.as_view(),name='borrow'),
   
]
