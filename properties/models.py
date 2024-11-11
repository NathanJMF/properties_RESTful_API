from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    number_of_rooms = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')

    def __str__(self):
        return f"{self.address}, {self.city}"
