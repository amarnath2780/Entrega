# Generated by Django 4.0.7 on 2022-08-31 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisemennt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IconAdd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(upload_to='images/add')),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]
