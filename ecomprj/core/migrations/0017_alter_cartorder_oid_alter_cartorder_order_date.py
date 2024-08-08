# Generated by Django 5.0.7 on 2024-08-07 10:03

import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_cartorder_oid_cartorder_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='oid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', blank=True, length=5, max_length=10, null=True, prefix=''),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]