from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from blog.models import Comment

from blog.validators import validate_password, validate_username


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