import random

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Count
from django.views.generic import CreateView

from userextend.forms import UserForm

class UserCreateView(CreateView):
    template_name = 'userextend/create_user.html'
    model = User
    form_class = UserForm
    success_url = '/login/'

    def form_valid(self, form):
            new_user = form.save(commit=False)
            new_user.first_name = new_user.first_name.upper()
            new_user.last_name = new_user.last_name.upper()
            random_sixnumber = random.randint(100000, 999999)
            new_user.username = f'{new_user.first_name.lower()[0]}{new_user.last_name.lower()}_{random_sixnumber}'
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()

            # # Trimitem un mail
            # subject = 'Contul BlogTube'
            # mesaj = (f"Buna seara, {new_user.first_name}, {new_user.last_name}\n\n"
            #          f"Bine ai venit in aplicatia noastra! Pentru autentificare ai nevoie de username-ul: {new_user.username}")
            #
            # send_mail(subject, mesaj, DEFAULT_FROM_EMAIL, [new_user.email])

            return super().form_valid(form)

def delete_users_with_duplicate_emails():
    duplicated_emails = User.objects.values('email') \
        .annotate(email_count=Count('email')) \
        .filter(email_count__gt=1) \
        .values_list('email', flat=True)

    for email in duplicated_emails:
        users_with_email = User.objects.filter(email=email).order_by('id')
        first_user = users_with_email.first()
        users_to_delete = users_with_email.exclude(id=first_user.id)
        users_to_delete.delete()

