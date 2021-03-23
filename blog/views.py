# from django.db.models.query_utils import Q
from django.conf import settings
from django.db.models import Q
from django.http.response import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post
from blog.models import Comment
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import CommentLike, Post, Category, PostSetting
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.views.generic import TemplateView, DetailView, RedirectView, ListView,UpdateView,CreateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from blog.forms import CommentForm,NewPostForm,NewPostSetForm
import json
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect

User = get_user_model()


class HomeView(ListView):
    paginate_by = 6
    template_name = 'blog/posts.html'
    queryset = Post.objects.filter(draft=False)
    context_object_name = 'posts'
   


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


@csrf_exempt
def create_comment(request):
    data = json.loads(request.body)
    user = request.user
    try:
        comment = Comment.objects.create(post_id=data['post_id'], content=data['content'], author=user)
        result = {"comment_id": comment.id, "content": comment.content, 'dislike_count': 0, 'like_count': 0,
                  'full_name': user.get_full_name()}
        return HttpResponse(json.dumps(result), status=201)
    except:
        result = {"error": 'error'}
        return HttpResponse(json.dumps(result), status=400)


class SinglePost(DetailView):
    model = Post
    template_name = 'blog/post_single.html'

    def get_object(self):
        slug = self.kwargs.get('pk')
        return get_object_or_404(Post.objects.select_related('post_setting', 'category', 'author'), slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        context['comments'] = post.comments.filter(post__slug = self.kwargs.get('pk'))
        context['settings'] = PostSetting.objects.get(post__slug = self.kwargs.get('pk'))
        context['form'] = CommentForm()
        return context


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


class AboutView(TemplateView):
    template_name = 'blog/about_us.html'



class SearchResultsView(ListView):
    model = Post
    template_name = 'search/searchbar.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(category__title__icontains=query)
        )
        return object_list


def search_view(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post = Post.objects.filter(Q(title__icontains=search))
        context = {'post': post}
        return render(request, 'search/searchbar.html', context)



def newpost(request):
    post_form = NewPostForm(initial={'author':request.user})
    setting_form = NewPostSetForm()

         

    if request.method == 'POST':
        post_form = NewPostForm(request.POST,request.FILES ,initial={'author':request.user})
        setting_form = NewPostSetForm(request.POST)

        if post_form.is_valid():
          
            title=post_form.cleaned_data['title']
            abstract=post_form.cleaned_data['abstract']
            promote=post_form.cleaned_data['promote']
            slug=post_form.cleaned_data['slug']
            content=post_form.cleaned_data['content']
            publish_time=post_form.cleaned_data['publish_time']
            draft=post_form.cleaned_data['draft']
            image=post_form.cleaned_data['image']
            category =post_form.cleaned_data['category']
            newpost = Post.objects.create(title=title,abstract= abstract,promote= promote,slug= slug,content= content,
            publish_time= publish_time,draft=draft, image= image,
            category= category,author=request.user )
            newpost.save()


    return render(request, 'blog/new_post_create.html', {
        'post_form': post_form,
        'setting_form' : setting_form
        
    })










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


# def single(request, pk):
#     try:
#         post = Post.objects.select_related('post_setting', 'category', 'author').get(slug=pk)
#         categories = Category.objects.all()
#     except Post.DoesNotExist:
#         raise Http404('post not found')
#     context = {
#         'form': CommentForm(),
#         "post": post,
#         'settings': post.post_setting,
#         'category': post.category,
#         'author': post.author,
#         'categories': categories,
#         'comments': post.comments.filter(is_confirmed=True)
#     }
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.post = post
#             comment.save()
#         else:
#             context['form'] = form
#
#     return render(request, 'blog/post_single.html', context)
