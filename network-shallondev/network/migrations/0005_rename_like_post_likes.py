# Generated by Django 4.2.7 on 2024-02-20 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_remove_post_likes_post_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='like',
            new_name='likes',
        ),
    ]
