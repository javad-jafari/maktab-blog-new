from django.urls import path, re_path
from .views import like_comment, single, SingleCategory
from .views import HomeView, LogoutView, RegisterView, AboutView, SinglePost, CategoresArchiveView
from django.contrib.auth.views import LoginView

urlpatterns = [

    path('posts/', HomeView.as_view(), name='posts_archive'),
    path('posts/<slug:pk>/', single, name='post_single'),
    path('categories/', CategoresArchiveView.as_view(), name='categories_archive'),
    path('categories/<slug:pk>/', SingleCategory.as_view(), name='category_single'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('about_us/', AboutView.as_view(), name='about'),
    path('like_comment/', like_comment, name='like_comment'),
    # path('posts/', home, name='posts_archive'),
    # path('posts/<slug:pk>/', SinglePost.as_view(), name='post_single'),
    # path('categories/', categories_archive, name='categories_archive'),
    # path('categories/<slug:pk>/', category_single, name='category_single'),
    # path('login/', login_view, name='login'),
    # path('logout/',logout_view,name='logout'),
    # path('register/', register_view, name='register'),
    # path('about_us/', about_view, name='about'),

]
