from django.urls import path
from .views import WalletOperation, WalletBalance

urlpatterns = [
    path('api/v1/wallets/<uuid:WALLET_UUID>/operation', WalletOperation.as_view(), name='wallet-operation'),
    path('api/v1/wallets/<uuid:WALLET_UUID>/', WalletBalance.as_view(), name='wallet-balance'),
]
