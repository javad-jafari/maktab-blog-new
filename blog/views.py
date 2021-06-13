# from django.db.models.query_utils import Q
from django.conf import settings
from django.db.models import Q
from django.db.models.fields import related
from blog.models import Post
from blog.models import Comment
from django.http import HttpResponse, request
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import CommentLike, Post, Category, PostSetting, RequestAuthor
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.views.generic import TemplateView, DetailView, ListView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from blog.forms import CommentForm,NewPostForm,NewPostSetForm
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator


User = get_user_model()


class HomeView(ListView):
    paginate_by = 9
    template_name = 'blog/index.html'
    queryset = Post.objects.filter(draft=False)
    context_object_name = 'posts'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promote'] = Post.objects.all()
        context['promote1'] = Post.objects.all()[1]
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
        return HttpResponse(json.dumps(result), status=401)


class SinglePost(DetailView):
    model = Post
    template_name = 'blog/post_single.html'

    def get_object(self):
        slug = self.kwargs.get('slug')
        item = get_object_or_404(Post.objects.select_related('post_setting', 'category', 'author'), slug=slug)
        item.incrementViewCount()
        return item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        related_comment = post.comments.filter(post__slug = self.kwargs.get('slug'),is_confirmed=True)
        paginator = Paginator(related_comment, 6) 
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['comments'] = page_obj
        context['settings'] = PostSetting.objects.get(post__slug = self.kwargs.get('slug'))
        context['form'] = CommentForm()
        return context


class SingleCategory(ListView):
    model = Post
    template_name = 'blog/post_archive_class.html'
    context_object_name = 'posts'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.filter(), slug=slug)
        posts = Post.objects.filter(category=category)
        paginator = Paginator(posts, 9)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj




class AboutView(TemplateView):
    template_name = 'blog/about_us.html'



class SearchResultsView(ListView):
    model = Post
    template_name = 'search/searchbar.html'

    def get_queryset(self):
        query = self.request.GET.get('search')

        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(category__title__icontains=query) | Q(slug__icontains=query)
        )
        return object_list


def search_view(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post = Post.objects.filter(Q(title__icontains=search))
        context = {'post': post}
        return render(request, 'search/searchbar.html', context)



@login_required(login_url='/accounts/login')
def newpost(request):
    post_form = NewPostForm(initial={'author':request.user})
         

    if request.method == 'POST':
        post_form = NewPostForm(request.POST,request.FILES ,initial={'author':request.user})

        if post_form.is_valid():
          
            new_post= post_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            PostSetting.objects.create(post_id=new_post.id,comment=True ,author=True ,allow_discussion=True)
            messages.success(request, _('ok you create it !'))
        else:
            messages.warning(request, _('something get wrong'))


    return render(request, 'profiles/new_post_create.html', {
        'post_form': post_form,
        
        
    })

@login_required(login_url='/accounts/login')
def post_update(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    post_form = NewPostForm(instance=post)
         

    if request.method == 'POST':
        post_form = NewPostForm(request.POST,request.FILES ,instance=post)

        if post_form.is_valid():

            post_form.save()
            messages.success(request, _('ok you update it !'))
        else:
            messages.warning(request, _('something get wrong'))


    return render(request, 'profiles/new_post_create.html', {
        'post_form': post_form,
        
        
    })





class BlogerPostView(DetailView):

    template_name = "blog/bloger_posts.html"

    def get_queryset(self) :
        return User.objects.filter(id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bloger_posts = Post.objects.filter(author__id=self.kwargs.get('pk'))
        paginator = Paginator(bloger_posts, 6) 
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context["author"] = User.objects.get(id=self.kwargs.get('pk'))
        context["posts"] = page_obj
        return context
    



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
