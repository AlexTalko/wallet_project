from uuid import uuid4

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Wallet


class WalletAPITests(APITestCase):

    def setUp(self):
        self.wallet_uuid = str(uuid4())
        self.wallet = Wallet.objects.create(uuid=self.wallet_uuid, balance=5000)

    def test_deposit(self):
        url = reverse('wallet-operation', kwargs={'WALLET_UUID': self.wallet_uuid})
        data = {
            'operationType': 'DEPOSIT',
            'amount': 1000
        }
        response = self.client.post(url, data, format='json')

        self.wallet.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.wallet.balance, 6000)

    def test_withdraw(self):
        url = reverse('wallet-operation', kwargs={'WALLET_UUID': self.wallet_uuid})
        data = {
            'operationType': 'WITHDRAW',
            'amount': 1000
        }
        response = self.client.post(url, data, format='json')

        self.wallet.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.wallet.balance, 4000)

    def test_get_wallet_balance(self):
        url = reverse('wallet-balance', kwargs={'WALLET_UUID': self.wallet_uuid})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], '5000.00')
