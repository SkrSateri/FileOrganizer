# Generated by Django 3.2.7 on 2021-09-20 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_alter_file_filecontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileBlob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileBlob', models.BinaryField()),
                ('fileExtention', models.CharField(max_length=10)),
            ],
        ),
    ]
