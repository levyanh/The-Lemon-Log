from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('reviews/<int:review_id>/', views.reviews_detail, name="review_detail"),
  path('reviews/<int:review_id>/comment/', views.add_comment_to_review, name="add_comment_to_review"),
  path('about/', views.about, name='about'),
  path('profile/', views.profile, name='profile'),
  path('accounts/signup/', views.signup, name='signup'),
  path('user_login/',views.user_login,name='user_login'),
  # path('comment/comment_id/approve/', views.comment_approve, name='comment_approve'),
  path('reviews/<int:review_id>/comment/<int:comment_id>/remove/', views.comment_remove, name='comment_remove'),
]

