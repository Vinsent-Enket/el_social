from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social.permissions import IsProprietor
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from transactions.services import create_stripe_product, get_payment_link, create_stripe_price
from users.permission import IsModerator


# Create your views here.

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
        request.user.wallet += price # TODO сделать это в виде периодической задачи которая будет проверять оплачен ли заказ
        request.user.save()
        return Response(url_to_pay)
