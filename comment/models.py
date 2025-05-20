from django.contrib.auth.models import User
from django.db import models

class Comment(models.Model):
    article = models.ForeignKey('Articol.Article', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"


class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', '👍'),
        ('dislike', '👎'),
        ('love', '❤️'),
        ('laugh', '😂'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment', 'reaction_type')

    def __str__(self):
        return f"{self.user.username} reacted {self.reaction_type} to comment {self.comment.id}"
