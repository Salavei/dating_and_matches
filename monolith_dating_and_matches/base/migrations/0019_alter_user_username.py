# Generated by Django 4.0.4 on 2023-05-15 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_alter_user_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=20, verbose_name='Name'),
        ),
    ]