from django.urls import path, include

from Articol import views
from .views import add_reaction

urlpatterns = [
    path('create_articol/', views.ArticolCreateView.as_view(), name='create-articol'),
    path('list_articol/', views.ArticolListView.as_view(), name='list-articol'),
    path('update_articol/<int:pk>', views.ArticolUpdateView.as_view(), name='update-articol'),
    path('delete_articol/<int:pk>', views.ArticolDeleteView.as_view(), name='delete-articol'),
    path('detail_articol/<int:pk>', views.ArticolDetailView.as_view(), name='details-articol'),
    path('comments/<int:comment_id>/react/<str:reaction_type>/', add_reaction, name='add-reaction'),

]