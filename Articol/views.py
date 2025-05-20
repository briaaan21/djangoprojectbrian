from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.views.generic.edit import FormMixin

from comment.models import Comment, Reaction
from .models import Article
from Articol.forms import ArticolForm, ArticolUpdateForm
from comment.forms import CommentForm


class ArticolCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticolForm
    template_name = 'Articol/create_articol.html'
    success_url = '/articles/list_articol/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticolUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticolUpdateForm
    template_name = 'Articol/update_articol.html'
    success_url = '/articles/list_articol/'

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author or self.request.user.is_superuser


class ArticolListView(ListView):
    model = Article
    template_name = 'Articol/list_articol.html'
    context_object_name = 'all_articles'


class ArticolDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'Articol/delete_articol.html'
    success_url = '/articles/list_articol/'

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author or self.request.user.is_superuser


class ArticolDetailView(FormMixin, DetailView):
    model = Article
    template_name = 'Articol/details_articol.html'
    form_class = CommentForm

    def get_success_url(self):
        return self.request.path

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.user = request.user
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comments.all().order_by('-date_posted').prefetch_related('reactions')

        user = self.request.user if self.request.user.is_authenticated else None

        comment_data = []
        for comment in comments:
            reactions_count = comment.reactions.values('reaction_type').annotate(count=Count('id'))
            reactions_count_dict = {r['reaction_type']: r['count'] for r in reactions_count}

            user_reactions = set()
            if user:
                user_reactions = set(comment.reactions.filter(user=user).values_list('reaction_type', flat=True))

            comment_data.append({
                'comment': comment,
                'reactions_count': reactions_count_dict,
                'user_reactions': user_reactions,
            })

        context['comment_data'] = comment_data
        context['form'] = self.get_form()
        context['user'] = user
        context['Reaction'] = Reaction
        return context


@login_required
@require_POST
def add_reaction(request, comment_id, reaction_type):
    valid_reactions = dict(Reaction.REACTION_CHOICES).keys()
    if reaction_type not in valid_reactions:
        comment = get_object_or_404(Comment, id=comment_id)
        return redirect('details-articol', pk=comment.article.id)

    comment = get_object_or_404(Comment, id=comment_id)
    reaction, created = Reaction.objects.get_or_create(
        user=request.user,
        comment=comment,
        reaction_type=reaction_type
    )
    if not created:
        reaction.delete()

    return redirect('details-articol', pk=comment.article.id)
