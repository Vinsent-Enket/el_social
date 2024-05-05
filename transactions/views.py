from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social.permissions import IsProprietor
from transactions.forms import TransactionForm
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from transactions.services import create_stripe_product, get_payment_link, create_stripe_price
from users.permission import IsModerator


# Create your views here.


class TransactionsListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transactions_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(payer=self.request.user).order_by('-id')


class TransactionsCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:transactions_list')

    def form_valid(self, form):
        price = form.cleaned_data.get('price')
        product_id = create_stripe_product(f'replenishment of the account by {price}$')
        # получаем из запроса на оплату id курса и получаем ссылку на прайс
        stripe_price_id = create_stripe_price(price=price, product_id=product_id)
        stripe_session = get_payment_link(stripe_price_id)
        url_to_pay = stripe_session['url']
        print(url_to_pay)
        form.instance.url_for_payment = url_to_pay

        self.request.user.wallet += form.instance.price
        self.request.user.save()
        form.instance.payer = self.request.user
        return super().form_valid(form)


class TransactionListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsProprietor | IsModerator]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class TransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def post(self, request, *args, **kwargs):
        """
        нужен прайс, покупатель
        :param serializer:
        :return:
        """
        price = self.request.data.get('price')
        product_id = create_stripe_product(f'replenishment of the account by {price}$')
        # получаем из запроса на оплату id курса и получаем ссылку на прайс
        stripe_price_id = create_stripe_price(price=price, product_id=product_id)
        stripe_session = get_payment_link(stripe_price_id)
        url_to_pay = stripe_session['url']
        transaction = Transaction.objects.create(price=price, payer=request.user)
        transaction.save()
        request.user.wallet += price  # TODO сделать это в виде периодической задачи которая будет проверять оплачен ли заказ
        request.user.save()
        return Response(url_to_pay)
