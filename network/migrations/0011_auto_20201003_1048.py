# Generated by Django 3.0.8 on 2020-10-03 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_auto_20201003_1045'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='post',
            new_name='postId',
        ),
    ]
