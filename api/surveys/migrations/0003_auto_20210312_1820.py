# Generated by Django 3.1 on 2021-03-12 15:20

import commons.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_auto_20210312_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=commons.models.NON_POLYMORPHIC_CASCADE, related_name='questions', to='surveys.survey', verbose_name='опрос'),
        ),
    ]
