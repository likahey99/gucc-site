# Generated by Django 2.2.28 on 2023-03-10 16:55

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('guccSite', '0003_auto_20230310_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='dateAdded',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 10, 16, 55, 30, 844134, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Gear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=128)),
                ('dateAdded', models.DateField()),
                ('picture', models.ImageField(default='gear_images/default.png', upload_to='')),
                ('colour', models.CharField(choices=[('green', 'GREEN'), ('blue', 'BLUE'), ('red', 'RED'), ('orange', 'ORANGE'), ('black', 'BLACK')], default='GREEN', max_length=6)),
                ('size', models.CharField(max_length=30)),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guccSite.Category')),
            ],
            options={
                'verbose_name_plural': 'Gear',
            },
        ),
    ]
