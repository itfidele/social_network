# Generated by Django 3.0.3 on 2020-02-22 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('makas', '0036_members_biography'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postlikes',
            name='like',
        ),
    ]