# Generated by Django 3.2.5 on 2023-07-19 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_api', '0005_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingListNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumber', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]