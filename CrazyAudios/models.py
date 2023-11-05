from django.db import models

# Create your models here.
class Audio(models.Model):
    name = models.CharField(max_length=72)
    upload_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % (self.name)