from django.db import models


class PropertySummary(models.Model):
       property_id = models.IntegerField()
       summary = models.TextField()

       def __str__(self):
           return f"Summary for Property ID {self.property_id}"



