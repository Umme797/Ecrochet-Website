# Generated by Django 5.1.2 on 2024-10-30 18:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecrochetapp', '0005_alter_pattern_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default='', max_length=1000, verbose_name='Shipping Address')),
                ('payment', models.CharField(choices=[('Credit Card', 'Credit Card'), ('Razor Pay', 'Razor Pay'), ('PayPal', 'PayPal'), ('UPI', 'UPI'), ('GPay', 'GPay')], max_length=50)),
                ('total', models.FloatField()),
                ('uid', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
