# Generated by Django 5.1.5 on 2025-01-20 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0002_donor_blood_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donor',
            name='blood_group',
            field=models.CharField(blank=True, choices=[('O%2B', 'O+'), ('O-', 'O-'), ('A%2B', 'A+'), ('A-', 'A-'), ('B%2B', 'B+'), ('B-', 'B-'), ('AB%2B', 'AB+'), ('AB-', 'AB-')], max_length=5, null=True),
        ),
    ]
