# Generated by Django 5.0 on 2024-02-24 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_alter_borrow_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrow',
            old_name='books',
            new_name='book',
        ),
        migrations.RemoveField(
            model_name='borrow',
            name='quantity',
        ),
    ]