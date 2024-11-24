from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet
from .serializers import OperationSerializer, WalletSerializer


class WalletOperation(APIView):

    @transaction.atomic
    def post(self, request, WALLET_UUID):
        wallet = Wallet.objects.filter(uuid=WALLET_UUID).first()
        if wallet is None:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            operation_type = serializer.validated_data['operationType']
            amount = serializer.validated_data['amount']

            try:
                if operation_type == 'DEPOSIT':
                    wallet.deposit(amount)
                else:
                    wallet.withdraw(amount)
                return Response({"balance": wallet.balance}, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletBalance(APIView):
    def get(self, request, WALLET_UUID):
        wallet = Wallet.objects.filter(uuid=WALLET_UUID).first()
        if wallet is None:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
