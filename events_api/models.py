from django.db import models

# Create your models here.
class Event(models.Model):
    name=models.TextField(null=False)
    datetime=models.DateTimeField(null=False)
    location=models.TextField(blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    def __str__(self):
        return str(self.name)
    class Meta:
        app_label = 'events_api'

