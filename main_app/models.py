from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # additional attributes
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username
    
class Review(models.Model):
    title = models.CharField(max_length=200)
    rating = models.IntegerField()
    description = models.TextField(max_length=2000)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default = False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text





    
