from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userfollowing")
    following = models.ManyToManyField(User, related_name="followedusers", blank=True)

    def serialize(self):
        user = self.user
        following = [user for user in self.following.all()]

    def __str__(self):
        return f"Followed by {self.user.username}"

class Comment(models.Model):
    commentedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userComments")
    commentedOn = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    
    def __str__(self):
        return f"{self.id} by: {self.commentedBy}"

class Like(models.Model):
    likedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likedPosts")
    likedOn = models.DateTimeField(auto_now_add=True)
    postId = models.IntegerField()

    def __str__(self):
        return f"{self.id} by: {self.likedBy}"

class Post(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment, related_name='postComments', blank=True)
    likes = models.ManyToManyField(Like, related_name="postLikes", blank=True)

    def __str__(self):
        return f"{self.message} by: {self.by}"

    def serialize(self):
        return {
            "id": self.id,
            "by": self.by,
            "message": self.message,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read": self.read,
            "likes": [{likes.likedBy, likes.likedOn} for likes in self.likes.all()],
            "comments": [{comment.comment, comment.commentedby, commentedOn} for comment in self.comments.all()],
        }

