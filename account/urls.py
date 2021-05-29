from django.urls import path, re_path
from .views import LogoutView, RegisterView,SignView,userprofile,change_password,ProfileUpdate
from .views import UserPassReset,PasswordResetComplete,PasswordResetConfirm,PasswordResetDone



urlpatterns = [

    path('login/', SignView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
	path('reset/', UserPassReset.as_view(), name='reset_pass'),
	path('reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
	path('confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
	path('confirm/done/', PasswordResetComplete.as_view(), name='password_reset_complete'),
	path('profile/',userprofile , name='profile'),
	path('password/', change_password, name='change_password'),
	path('profile/update/<uuid:pk>/',ProfileUpdate.as_view() , name='profile_update'),




]
