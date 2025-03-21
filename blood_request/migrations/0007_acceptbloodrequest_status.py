# Generated by Django 5.1.7 on 2025-03-13 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_request', '0006_acceptbloodrequest_request_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='acceptbloodrequest',
            name='status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('DONATED', 'donated'), ('CANCELED', 'canceled')], default='pending', max_length=10),
            preserve_default=False,
        ),
    ]
