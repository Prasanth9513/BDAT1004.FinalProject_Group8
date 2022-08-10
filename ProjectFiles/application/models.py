from django.db import models

# Create your models here.
class Exchange(models.Model):
    response_date=models.DateField()
    base=models.CharField(max_length=50)
    item=models.CharField(max_length=50)
    rate=models.FloatField()

    def __str__(self):
        return str(self.response_date)