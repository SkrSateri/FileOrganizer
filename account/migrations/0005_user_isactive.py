# Generated by Django 3.2.7 on 2021-10-01 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isActive',
            field=models.BooleanField(default=False),
        ),
    ]
