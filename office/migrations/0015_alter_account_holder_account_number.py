# Generated by Django 5.1.4 on 2024-12-30 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0014_rename_address_account_holder_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_holder',
            name='account_number',
            field=models.IntegerField(default=''),
        ),
    ]
