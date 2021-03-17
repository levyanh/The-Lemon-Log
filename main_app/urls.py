from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('reviews/<int:review_id>/', views.reviews_detail, name="review_detail"),
  path('about/', views.about, name='about'),
  path('profile/', views.profile, name='profile'),
  path('accounts/signup/', views.signup, name='signup'),
  path('user_login/',views.user_login,name='user_login'),
]

