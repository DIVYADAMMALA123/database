

# Create your models here.
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.BooleanField(default=True)  # True = Active, False = Inactive

    def __str__(self):
        return self.name
