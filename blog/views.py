from django import forms
from blog.forms import UserRegistrationForm
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Post, Category
from django.contrib.auth import login, logout, authenticate


def home(request):
    author = request.GET.get('author', None)
    category = request.GET.get('category', None)
    posts = Post.objects.all()
    posts_promot = Post.objects.filter(promote=True)[:3]

    if author:
        posts = posts.filter(author__username=author)
    if category:
        posts = posts.filter(category__slug=category)
    categories = Category.objects.all()
    context = {
        "posts": posts,
        "categories": categories,
        'posts_promot': posts_promot,
    }
    return render(request, 'blog/posts.html', context)


def single(request, pk):
    try:
        post = Post.objects.select_related('post_setting', 'category', 'author').get(slug=pk)
        categories = Category.objects.all()
    except Post.DoesNotExist:
        raise Http404('post not found')
    context = {
        "post": post,
        'settings': post.post_setting,
        'category': post.category,
        'author': post.author,
        'categories': categories,
        'comments': post.comments.filter(is_confirmed=True),
    }
    return render(request, 'blog/post_single.html', context)


def category_single(request, pk):
    try:
        category = Category.objects.get(slug=pk)
    except Category.DoesNotExist:
        raise Http404('Category not found')
    posts = Post.objects.filter(category=category)
    links = ''.join(
        '<li><a href={}>{}</a></li>'.format(reverse('post_single', args=[post.slug]), post.title) for post in posts)
    blog = '<html><head><title>post archive</title></head>{}<a href={}>all categories</a></body></html>'.format(
        '<ul>{}</ul>'.format(links), reverse('categories_archive'))
    return HttpResponse(blog)


def categories_archive(request):
    categories = Category.objects.all()
    links = ''.join(
        '<li><a href={}>{}</a></li>'.format(reverse('category_single', args=[category.slug]), category.title) for
        category in categories)
    blog = '<html><head><title>post archive</title></head>{}</body></html>'.format(
        '<ul>{}</ul>'.format(links))
    return HttpResponse(blog)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('posts_archive')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect('posts_archive')
    else:
        pass
    return render(request, 'blog/login.html', context={})


def logout_view(request):
    logout(request)
    return redirect('posts_archive')


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('valid')
        else:
            print('unvalid')
        context = {'form': form}
    else:
        form = UserRegistrationForm()
        context = {'form': form}

    return render(request, 'blog/register.html', context)
