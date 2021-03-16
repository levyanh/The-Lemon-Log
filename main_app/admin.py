from django.contrib import admin
from .models import Review, Comment, UserProfileInfo
# Register your models here.

admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(UserProfileInfo)
