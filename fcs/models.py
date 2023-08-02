from django.db import models

class FundCompany(models.Model):
    fund_name = models.CharField(max_length=255)
    cik_id = models.CharField(max_length=10)

    def __str__(self):
        return self.fund_name

class Filling(models.Model):
    cik_id = models.CharField(max_length=10)

    name_of_issuer = models.CharField(max_length=255)
    cusip = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=20, decimal_places=2)
    shares = models.CharField(max_length=100)
    investment_discretion = models.CharField(max_length=20)
    voting_info = models.CharField(max_length=100)
    quarter_info = models.CharField(max_length=100, default="NA")

    def __str__(self):
        return f"CIK: {self.cik_id}"
    
