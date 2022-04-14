from django.db import models

# Create your models here.
class Contact(models.Model):
    
    # contact module for storing the feedback given by the user to save to database
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self) -> str:
        return self.name
