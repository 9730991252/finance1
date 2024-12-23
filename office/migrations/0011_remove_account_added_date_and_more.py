# Generated by Django 5.1.1 on 2024-12-21 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0010_remove_saving_account_account_holder_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='added_date',
        ),
        migrations.RemoveField(
            model_name='account',
            name='collected_by',
        ),
        migrations.RemoveField(
            model_name='account',
            name='credit_amount',
        ),
        migrations.RemoveField(
            model_name='account',
            name='date',
        ),
        migrations.RemoveField(
            model_name='account',
            name='debit_amount',
        ),
        migrations.RemoveField(
            model_name='account',
            name='remark',
        ),
        migrations.AddField(
            model_name='account',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_amount', models.FloatField(null=True)),
                ('debit_amount', models.FloatField(null=True)),
                ('remark', models.CharField(default='', max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('account_holder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='office.account_holder')),
                ('collected_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='office.office_employee')),
            ],
        ),
    ]
