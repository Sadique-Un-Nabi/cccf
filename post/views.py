from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from .models import Post

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'post/home.html'  # Change to your template name
    context_object_name = "posts"
    ordering = ['-date_created']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Posts'
        return context


class PostCreateView(CreateView):
    model = Post
    template_name = 'post/post_form.html'  # Create a template for the form
    fields = ['title', 'content']  # Fields to be displayed in the form

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post:detail', kwargs={'pk': self.object.pk})
  

class PostDetailView(DetailView):
	model = Post