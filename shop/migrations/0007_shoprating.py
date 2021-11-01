# Generated by Django 3.1.6 on 2021-10-30 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_productrating'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(default=0)),
                ('comment', models.CharField(default='', max_length=500)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.seller')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
