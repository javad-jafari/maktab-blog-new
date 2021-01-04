from django.urls import path, re_path
from .views import like_comment, SingleCategory, SinglePost, search_view, SearchResultsView
from .views import HomeView, AboutView, CategoresArchiveView, create_comment
from .api import post_list, post_detail, comment_list, comment_detail

urlpatterns = [

    path('posts/', HomeView.as_view(), name='posts_archive'),
    path('posts/<slug:pk>/', SinglePost.as_view(), name='post_single'),
    path('categories/', CategoresArchiveView.as_view(), name='categories_archive'),
    path('categories/<slug:pk>/', SingleCategory.as_view(), name='category_single'),
    path('about_us/', AboutView.as_view(), name='about'),
    path('like_comment/', like_comment, name='like_comment'),
    path('comments/', create_comment, name='add_comment'),
    path('searchbar/', SearchResultsView.as_view(), name='searchbar'),
    path('comments/', create_comment, name='add_comment'),
    path('json/posts/', post_list, name='post_list'),
    path('json/comments/', comment_list, name='comment_list'),
    path('json/posts/<int:pk>/', post_detail, name='post_detail'),
    path('json/comments/<int:pk>/', comment_detail, name='comment_detail'),

    # path('posts/<slug:pk>/', single, name='post_single'),
    # path('posts/', home, name='posts_archive'),
    # path('categories/', categories_archive, name='categories_archive'),
    # path('categories/<slug:pk>/', category_single, name='category_single'),
    # path('login/', login_view, name='login'),
    # path('logout/',logout_view,name='logout'),
    # path('register/', register_view, name='register'),
    # path('about_us/', about_view, name='about'),
    # path('searchbar/', search_view, name='searchbar'),
]
