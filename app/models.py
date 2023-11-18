from django.db import models

# Create your models here.
class Dataviz(models.Model):
  d = models.JSONField()

  class Meta:
        db_table = 'json_data'

class Contact(models.Model):
    name = models.CharField(max_length=122,null= False, blank=True)
    email = models.CharField(max_length=122,null= False, blank=True)
    phone = models.CharField(max_length=12,null= False, blank=True)
    desc = models.TextField(null= False, blank=True)
    date = models.DateField(null= False, blank=True)

    def __str__(self):
        return self.name