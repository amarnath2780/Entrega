# Generated by Django 4.0.7 on 2022-09-19 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisemennt', '0003_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logo',
            name='image',
            field=models.ImageField(upload_to='images/logo'),
        ),
    ]
