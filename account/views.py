from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
from account.forms import UserThirdRegistrationForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

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
        if request.user.is_authenticated:
            return redirect('posts_archive')
        return render(request, 'registration/register.html', {'form': UserThirdRegistrationForm})

    def post(self, request):
        form = UserThirdRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect(reverse('login'))

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

class Profile(DeleteView):
    model = User
    template_name ='blog/profile.html'
    
    