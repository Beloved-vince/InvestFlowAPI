from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Request(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    repayment_period = models.PositiveIntegerField(help_text="Repayment period in months")
    purpose = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('funded', 'Funded'), ('repaid', 'Repaid')], default='pending')


class Funding(models.Model):
    lender = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_request = models.ForeignKey(Request, on_delete=models.CASCADE)
    amount_funded = models.DecimalField(max_digits=10, decimal_places=2)
    funded_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    loan_request = models.ForeignKey(Request, on_delete=models.CASCADE)
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)