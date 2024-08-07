# Generated by Django 5.0.7 on 2024-08-06 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.CharField(default='XYZ@gmail.com', max_length=50)),
                ('phone', models.CharField(default='+123 (456) 789', max_length=50)),
                ('subject', models.CharField(default='Help!', max_length=50)),
                ('message', models.TextField()),
            ],
            options={
                'verbose_name': 'Contact Us',
                'verbose_name_plural': 'Contact Us',
            },
        ),
    ]
