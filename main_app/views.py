from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileInfoForm, UserUpdateForm,ProfileUpdateForm, CommentForm, CommentUpdateForm, ReviewForm
from .models import Profile, Review, Comment, Photo
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
import uuid
import boto3

# Add these "constants" below the imports
S3_BASE_URL = 'https://s3-ap-southeast-1.amazonaws.com/'
BUCKET = 'lemonlogtech1'

# add photo to posts
def add_photo(request, review_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            print(url)
            # we can assign to review_id or review (if you have a review object)
            photo = Photo(url=url, review_id=review_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('review_detail', review_id=review_id)

# Add home view:
def home(request):
    review = Review.objects.all()
    paginator = Paginator(review, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html',{"page_obj":page_obj})
  
# Add review_detail:
def reviews_detail(request, review_id):
  review = get_object_or_404(Review, id=review_id)
  # comments = review.comments.filter(active=True)
  comments = review.comments.all()
  context = {
    "comments" : comments,
    "review" : review,
  }  
  return render(request, "reviews/review_detail.html", context)

# Add comments to review
@login_required
def add_comment_to_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    comment_form = CommentForm(request.POST or None)
    comment_form.instance.user = request.user
    if request.POST and comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.review = review
        new_comment.save()
        return redirect('review_detail',review_id=review_id)
    else:
        comment_form = CommentForm()
    return render(request, 'reviews/review_comments.html', {"comment_form" : comment_form})

# edit comments
@login_required
def comment_edit(request, review_id, comment_id):
    review = get_object_or_404(Review, id=review_id)
    comment = get_object_or_404(Comment, id=comment_id)
    comment_form = CommentUpdateForm(request.POST or None,instance=comment)
    if request.POST and comment_form.is_valid():
          comment_form.save()
          return redirect('review_detail',review_id=review_id)
    else:
        comment_form = CommentUpdateForm()
    return render(request, 'comments/edit_comments.html', {"comment_form" : comment_form})

# delete comments
@login_required
def comment_remove(request, review_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    review_id = comment.review.id
    if request.method == 'POST':
      comment.delete()
      return redirect('review_detail', review_id=review_id)
    else:
      return render(request,'comments/comment_delete.html')

# Add about view:
def about(request):
    return render(request,'about.html')

# Add profile view:
@login_required
def profile(request):
  review = Review.objects.filter(author= request.user.id)
  comment = Comment.objects.filter(user=request.user)
  if request.method == 'POST':
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
  
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      return redirect('profile')
  else:
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
  
  context = {
    'comments' : comment,
    'reviews' : review,
    'u_form' : u_form,
    'p_form' : p_form
  }
  return render(request, 'profile.html',context)

##################################
# USER - LOGIN - SIGNUP
##################################
# Add signup view:
def signup(request):
  registered = False
  if request.method == 'POST':
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileInfoForm(data=request.POST)
    if user_form.is_valid() and profile_form.is_valid():   
      # Save User Form to Database
      user = user_form.save()
      # Hash the password
      user.set_password(user.password)
      # Update with Hashed password
      user.save()
      # Now we deal with the extra info!
      # Can't commit yet because we still need to manipulate
      profile = profile_form.save(commit=False)
      # Set One to One relationship between
      # UserForm and UserProfileInfoForm
      profile.user = user
      # Check if they provided a profile picture
      if 'profile_pic' in request.FILES:
        print('found it')
        # If yes, then grab it from the POST form reply
        profile.profile_pic = request.FILES['profile_pic']
        # Registration Successful!
        registered = True
      else:
        print(user_form.errors,profile_form.errors)
      profile.save()
      login(request,user)
      return redirect('profile')
  else:
    user_form = UserForm()
    profile_form = UserProfileInfoForm()
  context = {'user_form': user_form, 'profile_form':profile_form, 'registered':registered}
  return render(request, 'registration/signup.html', context)

# views for login page

def user_login(request):

  if request.method == "POST":
    # First username and password
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    # Django's built-in authentication function:
    user = authenticate(username=username,password=password,email=email)

    if user:
      # Check it the account is active
      if user.is_active:
        # log the user in.
        login(request,user)
        # send the user back to some page
        # in this case their homepage
        return HttpResponseRedirect(reverse('profile'))
      else:
        # If account is not active:
        return HttpResponse("Your account is not active.")
    else:
      print("Someone tried to login and failed.")
      print("They used username: {}, email: {} and password: {}".format(username,email,password))
      return HttpResponse("Invalid login details supplied.")

  else:
      #Nothing has been provided for username or password.
      return render(request, 'registration/login.html', {})

##################################
# CREATE - EDIT - DELETE - REVIEWS
##################################

# create new review
@login_required
def review_new(request):
      review_form = ReviewForm(request.POST or None)
      if request.POST and review_form.is_valid:
          new_review = review_form.save(commit=False)
          new_review.author = request.user
          if 'review_image' in request.FILES:
            print('found it')
            new_review.review_image = request.FILES['review_image']
          else:
            print("errors")
          new_review.save()
          return redirect('home')
      else:
            return render(request, "reviews/review_new.html", {"review_form" : review_form})

# edit a review
@login_required
def review_edit(request, review_id):
      review = Review.objects.get(id=review_id)
      review_form = ReviewForm(request.POST or None, instance=review)
      if request.POST and review_form.is_valid:
          new_review = review_form.save(commit=False)
          if 'review_image' in request.FILES:
              print('found it')
              new_review.review_image = request.FILES['review_image']
          else:
            print("errors")
          review_form.save()
          return redirect('review_detail',review_id=review_id)
      else:
            return render(request, 'reviews/review_edit.html',{'review':review,'review_form':review_form})

# delete a review
@login_required
def review_delete(request,review_id):
      if request.method == 'POST':
        Review.objects.get(id=review_id).delete()
        return redirect('home')
      else:
        return render(request, 'reviews/review_delete.html')


  