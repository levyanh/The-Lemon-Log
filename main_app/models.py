from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # additional attributes
    profile_pic = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return self.user.username
    
class Review(models.Model):
    title = models.CharField(max_length=200)
    rating = models.IntegerField()
    description = models.TextField(max_length=2000)
    review_image = models.ImageField(default='default2.jpg',upload_to="review_pics")
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
    user = models.ForeignKey(User,on_delete=models.CASCADE,editable=False)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default = False)

    def approve(self):
        self.approved_comment = True
        self.save()

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.user)





    
