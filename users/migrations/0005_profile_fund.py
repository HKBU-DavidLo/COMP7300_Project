# Generated by Django 3.1.7 on 2021-04-12 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210402_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fund',
            field=models.FloatField(default=0.0),
        ),
    ]
