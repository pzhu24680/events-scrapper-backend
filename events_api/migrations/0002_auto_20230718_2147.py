# Generated by Django 3.2.5 on 2023-07-18 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.TextField(null=True),
        ),
    ]