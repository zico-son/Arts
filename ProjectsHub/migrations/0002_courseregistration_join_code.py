# Generated by Django 4.2 on 2023-04-25 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectsHub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseregistration',
            name='join_code',
            field=models.CharField(blank=1, max_length=8, unique=1),
        ),
    ]