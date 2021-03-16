from django.db import models
from django.contrib.auth.models import User

# Create your models here.





# Add Review model:
class Review(models.Model):
    title = models.CharField(max_length=255)
    rating = models.FloatField(default=0)
    text = models.TextField(max_length=2000)
    image = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)