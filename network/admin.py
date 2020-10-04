from django.contrib import admin
from .models import Like, Post, Comment, Following

# Register your models here.
admin.site.register(Like)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Following)