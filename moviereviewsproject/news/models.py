from django.db import models

class News(models.Model):
    headline = models.CharField(default="", max_length=200)
    body = models.TextField()
    date=models.DateTimeField()
    
    def __str__(self):return self.headline
