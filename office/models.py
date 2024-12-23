from django.db import models

# Create your models here.
class Office_employee(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    pin = models.IntegerField()
    status = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
class Account_holder(models.Model):
    added_by = models.ForeignKey(Office_employee, on_delete=models.CASCADE, null=True)
    holder_name = models.CharField(max_length=100)
    mobile = models.IntegerField(null=True)
    pin = models.IntegerField(null=True)
    account_number = models.CharField(max_length=1000, default='')
    status = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)
    
class Account_type(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)

class Account(models.Model):
    account_holder = models.ForeignKey(Account_holder, on_delete=models.CASCADE, null=True)
    account_type = models.ForeignKey(Account_type, on_delete=models.CASCADE, null=True)
    status = models.IntegerField(default=1)

class Transition(models.Model):
    collected_by = models.ForeignKey(Office_employee, on_delete=models.CASCADE, null=True)
    account_holder = models.ForeignKey(Account_holder, on_delete=models.CASCADE, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    credit_amount = models.FloatField(null=True)
    debit_amount = models.FloatField(null=True)
    remark = models.CharField(max_length=100, default='')
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
