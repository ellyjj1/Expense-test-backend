from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.db import transaction
from .models import Transaction, TransactionTotals
from .serializers import TransactionSerializer

# Create your views here.

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-date')
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            new_transaction = serializer.save()
            self.update_totals(new_transaction.type, new_transaction.amount)

    def perform_update(self, serializer):
        with transaction.atomic():
            old_transaction = self.get_object()
            new_transaction = serializer.save()
            if old_transaction.type != new_transaction.type or old_transaction.amount != new_transaction.amount:
                self.update_totals(old_transaction.type, -old_transaction.amount)
                self.update_totals(new_transaction.type, new_transaction.amount)

    def perform_destroy(self, instance):
        with transaction.atomic():
            self.update_totals(instance.type, -instance.amount)
            instance.delete()

    def update_totals(self, transaction_type, amount):
        totals, _ = TransactionTotals.objects.get_or_create(id=1)
        if transaction_type == 'income':
            totals.total_income += amount
        else:
            totals.total_expense += amount
        totals.save()

    @action(detail=False, methods=['GET'])
    def totals(self, request):
        income_total = Transaction.objects.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense_total = Transaction.objects.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        
        return Response({
            'total_income': income_total,
            'total_expense': expense_total
        })
