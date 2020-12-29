from django.urls import path, re_path
from .views import LogoutView, RegisterView,SignView

urlpatterns = [

    path('login/', SignView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

]
