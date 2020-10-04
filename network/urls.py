
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path('following', views.following, name="following"),
    path('profile/<str:user_name>', views.userprofile, name="userprofile"),
    path('postinformation/<int:post_id>', views.postinformation, name="postinformation"),
    path('managefollowing/<str:user_name>', views.managefollowing, name="managefollowing"),
]
