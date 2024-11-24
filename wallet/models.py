from django.db import models
from django.core.exceptions import ValidationError
from django.db import transaction

class Wallet(models.Model):
    uuid = models.UUIDField(primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @transaction.atomic
    def deposit(self, amount):
        self.balance += amount
        self.save()

    @transaction.atomic
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValidationError('Insufficient funds')
        self.balance -= amount
        self.save()
