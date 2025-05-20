from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from Articol.models import Article
from .forms import CommentForm
from .models import Comment, Reaction

@login_required
@require_POST
def add_reaction(request, comment_id, reaction_type):
    valid_reactions = dict(Reaction.REACTION_CHOICES).keys()
    if reaction_type not in valid_reactions:
        comment = get_object_or_404(Comment, id=comment_id)
        return redirect('details-articol', pk=comment.article.id)

    comment = get_object_or_404(Comment, id=comment_id)
    reaction_qs = Reaction.objects.filter(user=request.user, comment=comment)

    if reaction_qs.exists():
        reaction = reaction_qs.first()
        if reaction.reaction_type == reaction_type:
            reaction.delete()
        else:
            reaction.reaction_type = reaction_type
            reaction.save()
    else:
        Reaction.objects.create(user=request.user, comment=comment, reaction_type=reaction_type)

    return redirect('details-articol', pk=comment.article.id)

