# Generated by Django 3.1 on 2021-03-17 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0006_auto_20210316_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='status',
        ),
    ]
