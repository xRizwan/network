# Generated by Django 3.0.8 on 2020-10-02 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20201002_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='postComments', to='network.Comment'),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='postLikes', to='network.Like'),
        ),
    ]
