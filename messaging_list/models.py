from django.db import models

# Create your models here.

class MessagingListNumber(models.Model):
    phoneNumber=models.TextField(null=False)
    def __str__(self):
        return str(self.phoneNumber)
    class Meta:
        app_label = 'messaging_list'