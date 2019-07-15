from django.db import models


class Fraud(models.Model):
    trans_details = models.CharField(max_length=120)
    date = models.DateField()
    acc_no = models.BigIntegerField(default=0)
    deposit_amt = models.FloatField()
    withdraw_amt = models.TextField()
    subset_size = models.IntegerField(default=0)
