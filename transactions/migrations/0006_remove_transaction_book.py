# Generated by Django 5.0 on 2024-02-24 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_transaction_book'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='book',
        ),
    ]