# Generated by Django 4.0.4 on 2022-05-23 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_message_options_user_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ph',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.photo'),
        ),
    ]
