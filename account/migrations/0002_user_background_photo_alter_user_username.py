# Generated by Django 4.1.1 on 2022-09-27 04:58

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='background_photo',
            field=models.ImageField(blank=True, null=True, upload_to=account.models.get_background_image_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
