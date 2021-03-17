from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, User
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileInfoForm, UserUpdateForm,ProfileUpdateForm, CommentForm
from .models import Profile, Review, Comment
from django.urls import reverse

# Add home view:
def home(request):
  review = Review.objects.all()
  return render(request, 'home.html',{"reviews":review})
# Add comment:
def new_comments(request):
      pass
# Add review_detail:
def reviews_detail(request, review_id):
  comment = Comment.objects.all()
  review = Review.objects.get(id=review_id)
  comment_form = CommentForm(request.POST or None)
  if request.POST and comment_form.is_valid():
      new_comment = comment_form.save(commit=False)
      new_comment.user = request.user
      new_comment.save()
      return redirect('review_detail')
  else:
    context = {
      "comments" : comment,
      "review" : review,
      "comment_form" : comment_form
    }  
  return render(request, "reviews/review_detail.html", context)
# Add about view:
def about(request):
    return render(request,'about.html')

# Add profile view:
@login_required
def profile(request):
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
    'u_form' : u_form,
    'p_form' : p_form
  }
  return render(request, 'profile.html',context)

# Add signup view:
def signup(request):
  registered = False
  if request.method == 'POST':
    # Get info from "both" forms
    # It appears as one form to the user on the .html page
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileInfoForm(data=request.POST)

    # Check to see both forms are valid
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
        # Now save model
        profile.save()
        # Registration Successful!
        registered = True
      else:
        # One of the forms was invalid if this else gets called.
        print(user_form.errors,profile_form.errors)
      login(request,user)
      return redirect('profile')
  else:
      # Was not an HTTP post so we just render the forms as blank.
    user_form = UserForm()
    profile_form = UserProfileInfoForm()
  # This is the render and context dictionary to feed
  # back to the registration.html file page.
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

