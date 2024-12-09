# Generated by Django 5.1.4 on 2024-12-09 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_remove_borrowrequest_unique_borrow_period_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='borrowrequest',
            name='unique_borrow_period',
        ),
        migrations.RemoveField(
            model_name='borrowrequest',
            name='user',
        ),
        migrations.AddConstraint(
            model_name='borrowrequest',
            constraint=models.UniqueConstraint(fields=('book', 'borrow_start_date', 'borrow_end_date'), name='unique_borrow_period'),
        ),
    ]
