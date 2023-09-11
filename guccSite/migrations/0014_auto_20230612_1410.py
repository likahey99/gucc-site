# Generated by Django 2.2.28 on 2023-06-12 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guccSite', '0013_pagecontents'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagecontents',
            name='title',
            field=models.TextField(default='Gear Store'),
        ),
        migrations.AlterField(
            model_name='pagecontents',
            name='contact_option',
            field=models.CharField(choices=[('logo-whatsapp', 'WhatsApp'), ('call-outline', 'Phone Number'), ('mail-outline', 'Email')], default='call-outline', max_length=128),
        ),
    ]
