# Generated by Django 5.1.1 on 2024-12-21 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0012_transition_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transition',
            old_name='Account',
            new_name='account',
        ),
    ]