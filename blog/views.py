from django import forms
from django.core import paginator
from blog.forms import UserRegistrationForm, UserLoginForm, UserSeconRegistrationForm, CommentForm,UserThirdRegistrationForm
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Post, Category
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage


def home(request):
    author = request.GET.get('author', None)
    category = request.GET.get('category', None)
    posts = Post.objects.all()[:9]
    posts_promot = Post.objects.filter(promote=True)[:3]
     # posts = Post.objects.all()
    # p = paginator(posts,9)
    # page_num = request.GET.get('page',1)

    # try:
    #     page = p.page(page_num)
    # except EmptyPage:
    #     page = p.page(1)

    if author:
        posts = posts.filter(author__username=author)
    if category:
        posts = posts.filter(category__slug=category)
    categories = Category.objects.all()
    context = {
        "posts": posts,
        "categories": categories,
        'posts_promot': posts_promot,
        # 'items' : page,
    }
    return render(request, 'blog/posts.html', context)


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


def logout_view(request):
    logout(request)
    return redirect('posts_archive')


# def register_view(request):
#     if request.method == 'POST':
#         form = UserSeconRegistrationForm(request.POST)
#         if form.is_valid():        
#             user = form.save(commit=False)
#             password = user.password
#             user.set_password(password)
#             user.save()
#             return redirect('login')

#         else:
#             print('unvalid')
#         context = {'form': form}
#     else:
#         form = UserSeconRegistrationForm()
#         context = {'form': form}

#     return render(request, 'blog/register.html', context)


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
            return render(request,'blog/posts.html',{'new_user': new_user})

    else:
        user_form = UserThirdRegistrationForm()
    return render(request,'blog/register.html',{'user_form': user_form})



