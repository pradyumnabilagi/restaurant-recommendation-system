# Generated by Django 3.2.1 on 2021-06-06 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capp', '0024_menu_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(default=0, upload_to='pics'),
            preserve_default=False,
        ),
    ]
