# Generated by Django 4.0.7 on 2022-09-01 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_variation_variation_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('variant', 'variant'), ('color', 'color')], max_length=100),
        ),
    ]
