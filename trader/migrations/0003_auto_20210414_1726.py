# Generated by Django 3.1.7 on 2021-04-14 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0002_auto_20210414_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='created',
            field=models.DateTimeField(editable=False),
        ),
    ]