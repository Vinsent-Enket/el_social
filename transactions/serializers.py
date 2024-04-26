from rest_framework import serializers, status
from rest_framework.response import Response

from transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        #exclude = ('payer', )
        fields = '__all__'




