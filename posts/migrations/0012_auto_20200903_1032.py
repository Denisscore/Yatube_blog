# Generated by Django 2.2.6 on 2020-09-03 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20200902_2345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='user_post',
            new_name='user',
        ),
    ]
