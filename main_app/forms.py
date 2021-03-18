from django import forms
from django.contrib.auth.models import User
from .models import Profile, Comment, Review

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")
        return cleaned_data

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ["profile_pic",]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_pic']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "review_image", "description","rating"]
