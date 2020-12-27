from django import forms
from blog.models import Comment
from blog.forms import (UserRegistrationForm,
                        UserLoginForm,
                        UserSeconRegistrationForm,
                        CommentForm,
                        UserThirdRegistrationForm)

from django.http import (HttpResponse,
                         Http404,
                         HttpResponseRedirect,
                         response)

from django.shortcuts import (get_object_or_404,
                              redirect,
                              render)
from django.urls import reverse
from .models import CommentLike, Post, Category
from django.contrib.auth import login, logout, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.views.generic import TemplateView, DetailView, RedirectView, ListView
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import PermissionDenied, ValidationError
from django.views import View


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
    result = {'like_count': comment.like_count, 'dislike_count': comment.dislike_count}

    return HttpResponse(json.dumps(result), status=201)


class SinglePost(DetailView):
    model = Post
    template_name = 'blog/post_single.html'

    def get_object(self):
        slug = self.kwargs.get('pk')
        return get_object_or_404(Post.objects.select_related('post_setting', 'category', 'author'), slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        context['comments'] = post.comments.all()
        context['settings'] = post.post_setting
        return context


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


class SingleCategory(ListView):
    model = Post
    template_name = 'blog/post_archive_class.html'
    context_object_name = 'posts'

    def get_queryset(self):
        slug = self.kwargs.get('pk')
        category = get_object_or_404(Category.objects.filter(), slug=slug)
        posts = Post.objects.filter(category=category)
        return posts


class CategoresArchiveView(ListView):
    context_object_name = 'categories'
    queryset = Category.objects.all()
    template_name = 'blog/categories.html'


class LogoutView(RedirectView):
    url = '/posts/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html', {'form': AuthenticationForm})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user is None:
                return render(
                    request,
                    'registration/login.html',
                    {'form': form, 'invalid_creds': True}
                )

            try:
                form.confirm_login_allowed(user)
            except ValidationError:
                return render(
                    request,
                    'registration/login.html',
                    {'form': form, 'invalid_creds': True}
                )
            login(request, user)

            return redirect(reverse('posts_archive'))


class RegisterView(View):
    def get(self, request):
        return render(request, 'registration/register.html', {'form': UserThirdRegistrationForm})

    def post(self, request):
        form = UserThirdRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect(reverse('login'))

        return render(request, 'registration/register.html', {'form': form})


class AboutView(TemplateView):
    template_name = 'blog/about_us.html'

# def about_view(request):
#     return render(request, 'blog/about_us.html' )

# def register_view(request):
#     if request.method == 'POST':
#         user_form = UserThirdRegistrationForm(request.POST)
#         if user_form.is_valid():
#             # Create a new user object but avoid saving it yet
#             new_user = user_form.save(commit=False)
#             # Set the chosen password
#             new_user.set_password(user_form.cleaned_data['password'])
#             # Save the User object
#             new_user.save()
#             return render(request, 'blog/posts.html', {'new_user': new_user})
#
#     else:
#         user_form = UserThirdRegistrationForm()
#     return render(request, 'blog/register.html', {'user_form': user_form})


# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('posts_archive')
#     if request.method == 'POST':
#         form = UserLoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request.POST, username=username, password=password)
#             if user and user.is_active:
#                 login(request, user)
#                 return redirect('posts_archive')
#             else:
#                 print('unvalid')
#                 context = {'form': form}
#     else:
#
#         form = UserLoginForm()
#     return render(request, 'blog/login.html', {'form': form})

# def categories_archive(request):
#     categories = Category.objects.all()
#     context = {
#         'categories': categories,
#     }
#     return render(request, 'blog/categories.html', context)


# def category_single(request, pk):
#     try:
#         category = Category.objects.get(slug=pk)
#     except Category.DoesNotExist:
#         raise Http404('Category not found')
#     posts = Post.objects.filter(category=category)
#
#     context = {
#         'posts': posts,
#         'category': category,
#     }
#
#     return render(request, 'blog/post_archive.html', context)
