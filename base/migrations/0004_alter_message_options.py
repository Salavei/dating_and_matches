# Generated by Django 4.0.4 on 2022-05-21 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_delete_emailverirecord_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-received_at']},
        ),
    ]
