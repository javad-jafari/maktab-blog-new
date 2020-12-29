from django.urls import path, re_path
from .views import like_comment, SingleCategory, SinglePost, search_view,SearchResultsView
from .views import HomeView, AboutView, CategoresArchiveView, create_comment

urlpatterns = [

    path('posts/', HomeView.as_view(), name='posts_archive'),
    path('posts/<slug:pk>/', SinglePost.as_view(), name='post_single'),
    # path('posts/<slug:pk>/', single, name='post_single'),
    path('categories/', CategoresArchiveView.as_view(), name='categories_archive'),
    path('categories/<slug:pk>/', SingleCategory.as_view(), name='category_single'),
    path('about_us/', AboutView.as_view(), name='about'),
    path('like_comment/', like_comment, name='like_comment'),
    # path('posts/', home, name='posts_archive'),
    path('comments/', create_comment, name='add_comment'),
    # path('searchbar/', search_view, name='searchbar'),
    path('searchbar/',SearchResultsView.as_view() , name='searchbar'),
    # path('categories/', categories_archive, name='categories_archive'),
    # path('categories/<slug:pk>/', category_single, name='category_single'),
    # path('login/', login_view, name='login'),
    # path('logout/',logout_view,name='logout'),
    # path('register/', register_view, name='register'),
    # path('about_us/', about_view, name='about'),

]
