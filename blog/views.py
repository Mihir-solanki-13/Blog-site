from operator import truediv
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
    ListView ,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    )
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by =  5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
         user = get_object_or_404(User, username=self.kwargs.get('username'))
         return Post.objects.filter(author=user)

class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']
   
   #give the instace the author who is log in
    def form_valid(self, form) : 
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

   #give the instace the author who is log in
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self) :
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = '/'
    def test_fun(self):
        post = self.get_object()
        if self.request.user ==post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


 