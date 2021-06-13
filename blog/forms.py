from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.base import Model
from django.forms import fields
from django.forms.widgets import ChoiceWidget
from django.utils.translation import ugettext_lazy as _
from blog.models import Category, Comment, Post, PostSetting
from django.contrib.auth.models import User
from blog.validators import validate_password, validate_username
from ckeditor.widgets import CKEditorWidget
import re
import datetime
from blog.models import Post
# User = get_user_model()

class UserRegistrationForm(forms.Form):
    username = forms.CharField(label=_('نام کاربری'), max_length=150, required=True,
                               widget=forms.TextInput(attrs={"class": "form-control", }))
    email = forms.EmailField(label=_('ایمیل'), required=True, widget=forms.EmailInput(attrs={"class": "form-control"}),
                             help_text=_('یه ایمیل معتبر وارد کنید جان مادرتون'))
    password = forms.CharField(label=_('کلمه عبور'), widget=forms.PasswordInput(attrs={"class": "form-control"}),
                               required=True)
    password2 = forms.CharField(label=_('بازم کلمه عبور'), widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                required=True)
    first_name = forms.CharField(label=_('نام'), widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label=_('نام خانوادگی'), widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean(self):
        password = self.cleaned_data.get('password', None)
        password2 = self.cleaned_data.get('password2', None)
        if password != password2:
            raise ValidationError(_("password don't match"), code='invalid')

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        validate_username(username)
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        validate_password(password)
        return password


class UserLoginForm(forms.Form):
    username = forms.CharField(label=_('نام کاربری'), max_length=150, required=True,
                               widget=forms.TextInput(attrs={"class": "form-control", }))

    password = forms.CharField(label=_('کلمه عبور'), widget=forms.PasswordInput(attrs={"class": "form-control"}),
                               required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        return password


class UserSeconRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        labels = {
            'username': _('نام کاربری'),
            "password": _('رمز عبور'),
            "email": _('ایمیل'),
            "first_name": _('نام'),
            "last_name": _('نام خانوادگی'),
        }
        fields = ["username", "password", "email", "first_name", "last_name"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {'content': _("Comment"), }
        widgets = {'content': forms.Textarea(attrs={ 'rows': 5 , 'placeholder': 'دیدگاه خود را وارد  کنید'})}


class UserThirdRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='رمزعبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمزعبور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': _('نام کاربری'),
            "email": _('ایمیل'),
            "first_name": _('نام'),
            "last_name": _('نام خانوادگی')
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']



#--------------------------------------------------------------------------------------------------
def get_today():
    return datetime.datetime.now().date()

def get_tomorrow():
    return (datetime.datetime.now() + datetime.timedelta(days=1)).date() 

TODAY = get_today
TOMORROW = get_tomorrow
DATE_SELECTION = (
        (TODAY, "Today"),
        (TOMORROW, "Tomorrow"),
    )

class NewPostForm(forms.ModelForm):
    publish_time = forms.DateField(input_formats=["%Y-%m-%d"], widget=forms.Select(choices=DATE_SELECTION))
    content = forms.CharField(label=_('content'), widget=CKEditorWidget)
    class Meta:
        model = Post
        exclude = ['author','seen','slug']
        

class NewPostSetForm(forms.ModelForm):
    class Meta:
        model = PostSetting   
        fields = '__all__'