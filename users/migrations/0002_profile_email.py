# Generated by Django 3.1.7 on 2021-04-02 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(blank=True, max_length=30, verbose_name='email'),
        ),
    ]