# Generated by Django 2.2.4 on 2020-04-18 12:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20200418_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='external_diameter_reference',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Pole float powinno zawierać liczbę całkowitą bądź zmiennoprzecinkową', regex='^([0-9]*|[0-9]*\\.\\d+)$')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='internal_diameter_reference',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Pole float powinno zawierać liczbę całkowitą bądź zmiennoprzecinkową', regex='^([0-9]*|[0-9]*\\.\\d+)$')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='length',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Pole float powinno zawierać liczbę całkowitą bądź zmiennoprzecinkową', regex='^([0-9]*|[0-9]*\\.\\d+)$')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Pole integer powinno zawierać liczbę całkowitą', regex='^[0-9]*$')]),
        ),
    ]
