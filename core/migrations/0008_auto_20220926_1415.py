# Generated by Django 3.1.3 on 2022-09-26 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_tandc_is_converted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tandc',
            name='is_converted',
        ),
        migrations.AddField(
            model_name='quotation',
            name='is_converted',
            field=models.BooleanField(default=False),
        ),
    ]