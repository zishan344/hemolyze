# Generated by Django 5.1.7 on 2025-03-13 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blood_request', '0002_rename_acceptrequest_acceptbloodrequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acceptbloodrequest',
            old_name='request',
            new_name='request_accept',
        ),
    ]
