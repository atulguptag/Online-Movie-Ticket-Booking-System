# Generated by Django 4.2.7 on 2024-04-17 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_reservation_ticket'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='showtime',
            new_name='show',
        ),
    ]