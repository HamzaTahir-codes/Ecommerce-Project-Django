# Generated by Django 5.0.7 on 2024-08-07 07:18

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_cartorder_address_cartorder_city_cartorder_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='oid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', blank=True, length=5, max_length=10, null=True, prefix='oid'),
        ),
        migrations.AddField(
            model_name='cartorder',
            name='sku',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', blank=True, length=5, max_length=10, null=True, prefix='sku'),
        ),
    ]
