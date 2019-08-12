from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Entry
from django.contrib.auth.models import User


class HomeView(ListView):
    model = Entry
    template_name = 'entries/index.html'
    context_object_name = 'blog_entries'
    ordering = ['-entry_date']
    paginate_by = 4


class UserEntryListView(ListView):
    model = Entry
    template_name = 'entries/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'blog_entries'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Entry.objects.filter(entry_author=user).order_by('-entry_date')


class EntryView(LoginRequiredMixin, DetailView):
    model = Entry
    template_name = 'entries/entry_detail.html'


class CreateEntryView(LoginRequiredMixin, CreateView):
    model = Entry
    template_name = 'entries/create_entry.html'
    fields = ['entry_title', 'entry_text']

    def form_valid(self, form):
        form.instance.entry_author = self.request.user
        return super().form_valid(form)


class UpdateEntryView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # new post
    model = Entry
    fields = ['entry_title', 'entry_text']

    def form_valid(self, form):  # set the new author login as the author
        form.instance.entry_author = self.request.user
        return super().form_valid(form)

    def test_func(self):  # to make sure only author can edit his/her post
        Entry = self.get_object()
        if self.request.user == Entry.entry_author:
            return True
        return False


class EntryDeleteView(DeleteView):  # to delete  post
    model = Entry
    success_url = '/'

    def test_func(self):  # to make sure only author can delete his/her post
        Entry = self.get_object()
        if self.request.user == Entry.entry_author:
            return True
        return False


def about(request):
    return render(request, 'entries/about.html', {'title': 'About'})


def welcome(request):
    return render(request, 'entries/welcome.html', {})
