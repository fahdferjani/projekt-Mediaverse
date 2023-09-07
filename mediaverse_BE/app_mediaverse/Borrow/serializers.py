from rest_framework import serializers

from core.models import BorrowTransaction


class BorrowTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowTransaction
        fields = '__all__'
