# Generated by Django 4.1.2 on 2022-10-15 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0004_delete_view'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='status',
        ),
        migrations.RemoveField(
            model_name='link',
            name='type',
        ),
    ]