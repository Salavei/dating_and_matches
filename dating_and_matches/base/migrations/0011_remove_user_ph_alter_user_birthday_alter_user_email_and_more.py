# Generated by Django 4.0.4 on 2023-01-24 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_message_message_alter_user_avatar_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='ph',
        ),
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.IntegerField(verbose_name='Your age'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=20, verbose_name='Your gender'),
        ),
        migrations.AlterField(
            model_name='user',
            name='hash',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='likes',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=20, unique=True, verbose_name='Name'),
        ),
    ]
