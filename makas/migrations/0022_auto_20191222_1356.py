# Generated by Django 3.0 on 2019-12-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makas', '0021_auto_20191218_2352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='images',
        ),
        migrations.AddField(
            model_name='posts',
            name='images',
            field=models.ManyToManyField(to='makas.PostImages'),
        ),
    ]