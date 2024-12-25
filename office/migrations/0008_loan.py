# Generated by Django 5.1.4 on 2024-12-21 05:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0007_alter_saving_account_added_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_amount', models.FloatField(null=True)),
                ('interest_percentage', models.FloatField(null=True)),
                ('minimum_installment', models.FloatField(null=True)),
                ('loan_status', models.IntegerField(default=1)),
                ('date', models.DateField(auto_now_add=True)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('account_holder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='office.account_holder')),
                ('loaned_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='office.office_employee')),
            ],
        ),
    ]