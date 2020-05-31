from django.db import models


# Create your models here.
class User(models.Model):
    name_field = models.CharField(max_length=25)
    hash_field = models.CharField(max_length=61)

    def __str__(self):
        return self.name_field
