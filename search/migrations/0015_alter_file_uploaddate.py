# Generated by Django 3.2.7 on 2021-09-22 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0014_alter_file_filecontent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='uploadDate',
            field=models.DateField(default=None),
        ),
    ]
