from django.db import models
from django.contrib.auth.models import User

# Add Profile model:
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avarta = models.ImageField()

# Add Review model:
class Review(models.Model):
    title = models.CharField(max_length=255)
    rating = models.FloatField(default=0)
    text = models.TextField(max_length=2000)
    image = models.ImageField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)