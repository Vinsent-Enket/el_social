from django.urls import path, reverse

from transactions.apps import TransactionsConfig
from transactions.views import TransactionListAPIView, TransactionAPIView

app_name = TransactionsConfig.name

urlpatterns = [path('list/', TransactionListAPIView.as_view(), name='transactions_list'),
               path('create/', TransactionAPIView.as_view(), name='transaction_create'),
               ]
