from django.urls import path
from .views import BorrowBookView,ReturnBookView,DepositMoneyView,TransactionReportView
urlpatterns = [
    path('deposit/',DepositMoneyView.as_view(),name='deposit'),
    path('report/',TransactionReportView.as_view(),name='report'),
    path('report/return/<int:transaction_id>/', ReturnBookView.as_view(), name='return'),

]
