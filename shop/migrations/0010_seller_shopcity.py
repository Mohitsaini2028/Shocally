# Generated by Django 3.1.6 on 2022-04-02 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_seller_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='shopCity',
            field=models.CharField(default='', max_length=150),
        ),
    ]
