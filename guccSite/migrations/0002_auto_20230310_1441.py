# Generated by Django 2.2.28 on 2023-03-10 14:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('guccSite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='dateAdded',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 10, 14, 41, 56, 341207, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default='profile_images/default.jpeg', upload_to='profile_images'),
        ),
    ]
