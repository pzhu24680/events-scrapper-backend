# Generated by Django 3.2.5 on 2023-07-18 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_api', '0002_auto_20230718_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='datetime',
            field=models.DateTimeField(),
        ),
    ]