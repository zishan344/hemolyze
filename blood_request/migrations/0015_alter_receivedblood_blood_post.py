# Generated by Django 5.1.7 on 2025-03-13 06:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_request', '0014_alter_receivedblood_blood_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receivedblood',
            name='blood_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blood_post', to='blood_request.bloodrequest'),
        ),
    ]
