# Generated by Django 3.0 on 2023-04-02 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='address',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='orders',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=15),
        ),
    ]