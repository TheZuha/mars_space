from django.db import models

from users.models import Student


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="blog_images/")
    author = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='blog_author')
    created_at = models.DateTimeField(auto_now_add=True)



class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    liker = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)