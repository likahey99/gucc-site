# Generated by Django 2.2 on 2023-03-10 16:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gearStore', '0003_auto_20230310_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='dateAdded',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 10, 16, 40, 54, 293690, tzinfo=utc)),
        ),
    ]
