from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from django.db.models import Sum
from django.db import transaction
from .models import Transaction, TransactionTotals
from .serializers import TransactionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-date')
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]  # 添加此行以限制访问

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


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    print("Register view reached")
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    user.save()

    return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
