# from django.db import models

# class PropertySummary(models.Model):
#     property_id = models.OneToOneField('myapp.Property', on_delete=models.CASCADE)
#     summary = models.TextField()

#     def __str__(self):
#         return f"Summary for Property ID {self.property.id}"

from django.db import models

class PropertySummary(models.Model):
    property_id = models.IntegerField()  # Stores property ID as an integer
    summary = models.TextField()  # Stores the summary text

    def __str__(self):
        return f"Summary for Property ID {self.property_id}"