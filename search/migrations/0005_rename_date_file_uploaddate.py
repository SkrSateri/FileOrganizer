# Generated by Django 3.2.7 on 2021-09-20 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_auto_20210920_0631'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='date',
            new_name='uploadDate',
        ),
    ]
