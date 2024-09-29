from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from transactions.models import Transaction  # Change this line

class TransactionViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.transaction_url = reverse('transaction-list')
        self.totals_url = reverse('transaction-totals')
        
        # Create some test transactions
        Transaction.objects.create(description="Salary", amount=5000, type="income")
        Transaction.objects.create(description="Rent", amount=1000, type="expense")
        Transaction.objects.create(description="Groceries", amount=200, type="expense")

    def test_get_all_transactions(self):
        response = self.client.get(self.transaction_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_transaction(self):
        data = {"description": "New laptop", "amount": 1500, "type": "expense"}
        response = self.client.post(self.transaction_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 4)

    def test_get_single_transaction(self):
        transaction = Transaction.objects.first()
        response = self.client.get(f"{self.transaction_url}{transaction.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], transaction.description)

    def test_update_transaction(self):
        transaction = Transaction.objects.first()
        data = {"description": "Updated description", "amount": 5500, "type": "income"}
        response = self.client.put(f"{self.transaction_url}{transaction.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transaction.objects.get(id=transaction.id).description, "Updated description")

    def test_delete_transaction(self):
        transaction = Transaction.objects.first()
        response = self.client.delete(f"{self.transaction_url}{transaction.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 2)

    def test_get_totals(self):
        response = self.client.get(self.totals_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_income'], Decimal('5000.00'))
        self.assertEqual(response.data['total_expense'], Decimal('1200.00'))

    def test_totals_after_adding_transaction(self):
        data = {"description": "Bonus", "amount": 1000, "type": "income"}
        self.client.post(self.transaction_url, data)
        response = self.client.get(self.totals_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_income'], Decimal('6000.00'))
        self.assertEqual(response.data['total_expense'], Decimal('1200.00'))

    def test_totals_after_deleting_transaction(self):
        transaction = Transaction.objects.filter(type="expense").first()
        self.client.delete(f"{self.transaction_url}{transaction.id}/")
        response = self.client.get(self.totals_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_income'], Decimal('5000.00'))
        self.assertEqual(response.data['total_expense'], Decimal('200.00'))