from django import forms
from blog.models import Comment
from django.core import paginator
from blog.forms import UserRegistrationForm, UserLoginForm, UserSeconRegistrationForm, CommentForm, \
    UserThirdRegistrationForm
from django.http import HttpResponse, Http404, HttpResponseRedirect, response
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import CommentLike, Post, Category
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import TemplateView, DetailView, View, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
import json


class HomeView(TemplateView):
    template_name = 'blog/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(draft=False)[:9]
        context['category'] = Category.objects.all()
        context['posts_promot'] = Post.objects.filter(promote=True)[:3]
        return context


@csrf_exempt
def like_comment(request):
    data = json.loads(request.body)
    user = request.user
    try:
        comment = Comment.objects.get(id=data['comment_id'])
    except Comment.DoesNotExist:
        return HttpResponse('bad request', status=404)
    try:
        comment_like = CommentLike.objects.get(author=user, comment=comment)
        comment_like.condition = data['condition']
        comment_like.save()
    except CommentLike.DoesNotExist:
        CommentLike.objects.create(author=user, condition=data['condition'], comment=comment)
    response = {'like_count': comment.like_count, 'dislike_count': comment.dislike_count}

    return HttpResponse(json.dumps(response), status=201)


# class SinglePost(DetailView):
#     model = Post
#     template_name = 'blog/post_single_class.html'

#     def get_object(self):
#         slug = self.kwargs.get('slug')
#         return get_object_or_404(Post.objects.select_related('post_setting', 'category', 'author'),slug=slug)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs) 
#         post = context['post']
#         context['comments'] = post.comments.all()
#         context['settings'] = post.post_setting
#         context['form'] = CommentForm()
#         return context


def single(request, pk):
    try:
        post = Post.objects.select_related('post_setting', 'category', 'author').get(slug=pk)
        categories = Category.objects.all()
    except Post.DoesNotExist:
        raise Http404('post not found')
    context = {
        'form': CommentForm(),
        "post": post,
        'settings': post.post_setting,
        'category': post.category,
        'author': post.author,
        'categories': categories,
        'comments': post.comments.filter(is_confirmed=True)
    }
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        else:
            context['form'] = form

    return render(request, 'blog/post_single.html', context)


def category_single(request, pk):
    try:
        category = Category.objects.get(slug=pk)
    except Category.DoesNotExist:
        raise Http404('Category not found')
    posts = Post.objects.filter(category=category)

    context = {
        'posts': posts,
        'category': category,
    }

    return render(request, 'blog/post_archive.html', context)


def categories_archive(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'blog/categories.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('posts_archive')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request.POST, username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('posts_archive')
            else:
                print('unvalid')
                context = {'form': form}
    else:

        form = UserLoginForm()
    return render(request, 'blog/login.html', {'form': form})


class LogoutView(RedirectView):
 
    url = '/posts/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


def about_view(request):
    return render(request, 'blog/about_us.html')


def register_view(request):
    if request.method == 'POST':
        user_form = UserThirdRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'blog/posts.html', {'new_user': new_user})

    else:
        user_form = UserThirdRegistrationForm()
    return render(request, 'blog/register.html', {'user_form': user_form})
