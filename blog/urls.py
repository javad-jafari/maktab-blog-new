from django.urls import path, re_path
from .views import categories_archive, category_single, register_view, about_view, like_comment
from .views import HomeView, LogoutView, login_view, single

urlpatterns = [
    # path('posts/', home, name='posts_archive'),
    path('posts/', HomeView.as_view(), name='posts_archive'),
    path('posts/<slug:pk>/', single, name='post_single'),
    # path('posts/<slug:slug>/', SinglePost.as_view(), name='post_single'),
    path('categories/', categories_archive, name='categories_archive'),
    path('categories/<slug:pk>/', category_single, name='category_single'),
    path('login/', login_view, name='login'),
    # path('login/',LoginView,name='login'),
    # path('logout/',logout_view,name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('about_us/', about_view, name='about'),
    path('like_comment/', like_comment, name='like_comment'),

]
