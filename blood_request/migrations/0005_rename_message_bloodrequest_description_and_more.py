# Generated by Django 5.1.7 on 2025-03-13 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blood_request', '0004_remove_bloodrequest_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloodrequest',
            old_name='message',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='bloodrequest',
            name='state',
        ),
    ]
