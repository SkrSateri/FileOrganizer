# Generated by Django 3.2.7 on 2021-09-20 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0010_alter_file_filecontent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='fileContent',
            field=models.FileField(upload_to=''),
        ),
    ]
