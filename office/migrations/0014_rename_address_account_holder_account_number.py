# Generated by Django 5.1.4 on 2024-12-23 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0013_rename_account_transition_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account_holder',
            old_name='address',
            new_name='account_number',
        ),
    ]
