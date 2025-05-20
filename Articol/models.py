from django.contrib.auth.models import User
from django.db import models

from comment.models import Comment


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='articol_images/', blank=True, null=True)

    def __str__(self):
        return f"Article: {self.title} - By {self.author.username}"

