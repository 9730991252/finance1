# Generated by Django 5.1.1 on 2024-12-21 12:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0011_remove_account_added_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transition',
            name='Account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='office.account'),
        ),
    ]