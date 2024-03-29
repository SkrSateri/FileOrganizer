from django.db import models

# Create your models here.

class File(models.Model): #Model for files datatable
    fileName = models.CharField(max_length = 30)
    fileDescription = models.TextField(default = None)
    lastUploadBy = models.CharField(max_length = 50, default = None)
    uploadDate = models.DateField(default = None)
    fileContent = models.FileField(default = None, null = True)


class FileBlob(models.Model):
    fileBlob = models.BinaryField()
    fileExtention = models.CharField(max_length = 30)