from django.db import models


# Create your models here.

class File(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/%Y/%m/%d/')
    percentage = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    def __str__(self):
        return self.name

