from django import forms
from comment.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control animated-textarea',
                'placeholder': 'Write a comment...',
                'rows': 3,
                'maxlength': 500,
            }),
        }