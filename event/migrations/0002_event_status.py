# Generated by Django 5.1.5 on 2025-01-25 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('canceled', 'Canceled'), ('recieved', 'Recieved')], default='pending', max_length=10),
        ),
    ]
