# Generated by Django 3.2.7 on 2021-09-16 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='fileContent',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
