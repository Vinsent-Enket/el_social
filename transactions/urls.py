from django.urls import path, reverse

from transactions.apps import TransactionsConfig
from transactions.views import TransactionListAPIView, TransactionAPIView, TransactionsListView, TransactionsCreateView

app_name = TransactionsConfig.name

urlpatterns = [
    # path('list/', TransactionListAPIView.as_view(), name='transactions_list'),
    #                path('create/', TransactionAPIView.as_view(), name='transaction_create'),

    path('list/', TransactionsListView.as_view(), name='transactions_list'),
    path('create/', TransactionsCreateView.as_view(), name='transaction_create'),
]
