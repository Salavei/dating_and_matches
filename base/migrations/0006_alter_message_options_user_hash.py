# Generated by Django 4.0.4 on 2022-05-21 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={},
        ),
        migrations.AddField(
            model_name='user',
            name='hash',
            field=models.CharField(default=None, max_length=64, null=True, unique=True),
        ),
    ]
