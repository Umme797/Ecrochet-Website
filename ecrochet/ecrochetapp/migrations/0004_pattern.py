# Generated by Django 5.1.2 on 2024-10-30 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecrochetapp', '0003_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='Product Name')),
                ('description', models.TextField()),
                ('difficulty', models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], max_length=50)),
                ('patterndetails', models.CharField(max_length=50, verbose_name='Pattern Details')),
                ('pimage', models.ImageField(upload_to='image')),
            ],
        ),
    ]
