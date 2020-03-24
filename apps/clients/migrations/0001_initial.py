# Generated by Django 2.2.4 on 2020-03-16 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_sap_id', models.IntegerField(unique=True)),
                ('client_name', models.CharField(max_length=255)),
            ],
        ),
    ]