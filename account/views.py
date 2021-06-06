from django.contrib.auth import logout, authenticate, login, get_user_model,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.http.response import Http404,HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import RedirectView ,UpdateView
from account.forms import UserThirdRegistrationForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Category, Post ,Comment
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

User = get_user_model()


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SignView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = '/'




class RegisterView(View):
    def get(self, request):
        print(30*'*')
        print(request.META["HTTP_REFERER"])
        print(30*'*')
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'registration/register.html', {'form': UserThirdRegistrationForm})

    def post(self, request):
        form = UserThirdRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(request, user)
            return redirect('profile')

        return render(request, 'registration/register.html', {'form': form})




class UserPassReset(auth_views.PasswordResetView):
	template_name = 'registration/password_reset_form.html'
	success_url = reverse_lazy('password_reset_done')
	email_template_name = 'registration/password_reset_email.html'

class PasswordResetDone(auth_views.PasswordResetDoneView):
	template_name = 'registration/reset_done.html'

class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
	template_name = 'registration/password_reset_confirm.html'
	success_url = reverse_lazy('password_reset_complete')

class PasswordResetComplete(auth_views.PasswordResetCompleteView):
	template_name = 'registration/password_reset_complete.html'





@login_required(login_url='/accounts/login/')    
def userprofile(request):
    user = request.user.id
    
    if request.user.is_superuser:
        posts = Post.objects.all()

    else:
        posts = Post.objects.filter(author_id=user)  

    paginator = Paginator(posts, 2) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

        
    context = {
        'user':User.objects.get(id=user),
        'page_obj': page_obj,
    }
    return render(request, 'profiles/home.html', context)



@login_required(login_url='/accounts/login/')
def delete_post(request,post_id):

    ''' this function delete selected post from admin side '''

    if request.user.is_superuser:
        post = get_object_or_404(Post,id=post_id)
        if post:
            post.delete()
            messages.success(request, 'selected post was successfully delete!')
            return redirect('/accounts/profile/')
        else:
            Http404()
    else:
        raise PermissionDenied()

def draft_post(request,post_id):

    ''' this function get draft selected post from admin side '''

    if request.user.is_superuser:
        post = get_object_or_404(Post,id=post_id)
        if post:
            post.draft = True
            post.save()
            messages.success(request, 'selected post was successfully get draft!')
            return redirect('/accounts/profile/')
        else:
            Http404()
    else:
        raise PermissionDenied()



def publish_post(request,post_id):

    ''' this function get publish selected post from admin side '''

    if request.user.is_superuser:
        post = get_object_or_404(Post,id=post_id)
        if post:
            post.draft = False
            post.save()
            messages.success(request, 'selected post was successfully get publish!')
            return redirect('/accounts/profile/')
        else:
            Http404()
    else:
        raise PermissionDenied()
        




@login_required(login_url='/accounts/login/') 
def admin_all_users(request):
    user = request.user.id
    if request.user.is_superuser:
        users = User.objects.all()

    else:
        raise PermissionDenied()

    paginator = Paginator(users, 2) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

        
    context = {
        'user':User.objects.get(id=user),
        'page_obj': page_obj
     }
    return render(request, 'admin/all_users.html', context)   



@login_required(login_url='/accounts/login/') 
def admin_all_categories(request):
    if request.user.is_superuser:
        all_cat=Category.objects.all()
        paginator = Paginator(all_cat, 2) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context ={
        'categories': page_obj}
        return render(request, 'admin/all_categories.html', context)
    else:
        raise PermissionDenied()




@login_required(login_url='/accounts/login/') 
def admin_all_comments(request):
    if request.user.is_superuser:
        all_comment=Comment.objects.all()
        paginator = Paginator(all_comment, 2) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context ={
        'comments': page_obj}
        return render(request, 'admin/all_comments.html', context)
    else:
        raise PermissionDenied()




@login_required(login_url='/accounts/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/accounts/profile/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profiles/changepass.html', {
        'form': form
    })

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['full_name', "avatar"]
    template_name = 'profiles/profile.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('profile')
    def form_valid(self, form):
        form.instance.email = self.request.user.email
        return super().form_valid(form)



