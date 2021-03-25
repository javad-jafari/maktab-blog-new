from django.urls import path, re_path, include
from .views import like_comment, SingleCategory, SinglePost, search_view, SearchResultsView,newpost,post_set
from .views import HomeView, AboutView, CategoresArchiveView, create_comment,BlogerPostView
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
    path('posts/create/v1/', newpost, name='new_post'),
    path('posts/setting/create/v1/', post_set, name='new_post_set'),
    path('posts/bloger/v1/<int:pk>', BlogerPostView.as_view(), name='bloger_post'),




  
]
