# Generated by Django 3.1.6 on 2021-10-26 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookingitem',
            old_name='item_name',
            new_name='service_name',
        ),
    ]
