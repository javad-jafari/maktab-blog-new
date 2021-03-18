from django.urls import path, re_path, include
from .views import like_comment, SingleCategory, SinglePost, search_view, SearchResultsView
from .views import HomeView, AboutView, CategoresArchiveView, create_comment
from .api import CommentViewModel
# from .api import post_list, post_detail,comment_list, comment_detail
# from .api import PostView, PostDetailView
# from .api import PostList, PostDetail
# from .api import PostList1, PostDetail1
from .api import PostViewModel,CategoryViewModel
from rest_framework.routers import DefaultRouter
from zoomit.urls import router
# router = DefaultRouter()
router.register(r'posts', PostViewModel)
router.register(r'comments', CommentViewModel)
router.register(r'categories', CategoryViewModel)

urlpatterns = [

    path('', HomeView.as_view(), name='posts_archive'),
    path('posts/<slug:pk>/', SinglePost.as_view(), name='post_single'),
    path('categories/', CategoresArchiveView.as_view(), name='categories_archive'),
    path('categories/<slug:pk>/', SingleCategory.as_view(), name='category_single'),
    path('about_us/', AboutView.as_view(), name='about'),
    path('like_comment/', like_comment, name='like_comment'),
    path('comments/', create_comment, name='add_comment'),
    path('searchbar/', SearchResultsView.as_view(), name='searchbar'),
    path('comments/', create_comment, name='add_comment'),
    # path('json/', include(router.urls)),

    # path('json/comments/', comment_list, name='comment_list'),
    # path('json/comments/<int:pk>/', comment_detail, name='comment_detail'),
    # path('json/posts/', PostViewModel.as_view({'get': 'list', 'post': 'create'}), name='post_list'),
    # path('json/posts/<int:pk>/', PostViewModel.as_view({'get': 'retrieve',
    #                                                     'put': 'update',
    #                                                     'delete': 'destroy'}), name='post_detail'),
    # path('json/posts/', PostList1.as_view(), name='post_list'),
    # path('json/posts/<int:pk>/', PostDetail1.as_view(), name='post_detail'),
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
