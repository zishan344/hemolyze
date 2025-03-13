# Generated by Django 5.1.7 on 2025-03-13 05:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_request', '0007_acceptbloodrequest_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptbloodrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('donated', 'Donated'), ('canceled', 'Canceled')], default='pending', max_length=10),
        ),
        migrations.CreateModel(
            name='ReceivedBlood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('received', 'Received'), ('canceled', 'Canceled')], default='pending', max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donor', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
