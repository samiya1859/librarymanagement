# Generated by Django 5.0 on 2024-02-23 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_alter_transaction_balance_after_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
    ]