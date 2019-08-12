from django.urls import path
from .views import HomeView, EntryView, CreateEntryView, UpdateEntryView, EntryDeleteView, UserEntryListView
from . import views

urlpatterns = [
    path('home/', HomeView.as_view(), name='blog-home'),
    path('user/<str:username>', UserEntryListView.as_view(), name='user-posts'),
    path('entry/<int:pk>/', EntryView.as_view(), name="entry-detail"),
    path('create_entry/', CreateEntryView.as_view(success_url='/'), name="create_entry"),
    path('entry/<int:pk>/update', UpdateEntryView.as_view(), name='post-update'),
    path('entry/<int:pk>/delete', EntryDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('', views.welcome, name='welcome'),
]
