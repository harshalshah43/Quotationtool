# Generated by Django 3.1.3 on 2022-04-25 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20220425_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotationitems',
            name='margin',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
