from django.urls import path, re_path, include
from .views import like_comment, SingleCategory, SinglePost, search_view, SearchResultsView,newpost
from .views import HomeView, AboutView, create_comment,BlogerPostView,post_update
from .api import CommentViewModel
# from .api import post_list, post_detail,comment_list, comment_detail
# from .api import PostView, PostDetailView
# from .api import PostList, PostDetail
# from .api import PostList1, PostDetail1
from .api import PostViewModel,CategoryViewModel,PostSetViewModel
from rest_framework.routers import DefaultRouter
from zoomit.urls import router
# router = DefaultRouter()
router.register(r'posts', PostViewModel)
router.register(r'comments', CommentViewModel)
router.register(r'categories', CategoryViewModel)
router.register(r'settings', PostSetViewModel)


urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    re_path(r'posts/(?P<slug>[-\w]+)/', SinglePost.as_view(), name='post_single'),
    re_path(r'categories/(?P<slug>[-\w]+)/', SingleCategory.as_view(), name='category_single'),
    path('about_us/', AboutView.as_view(), name='about'),
    path('like_comment/', like_comment, name='like_comment'),
    path('comments/', create_comment, name='add_comment'),
    path('searchbar/', SearchResultsView.as_view(), name='searchbar'),
    path('comments/', create_comment, name='add_comment'),
    path('post/create/v1/', newpost, name='new_post'),
    path('post/update/v1/<int:post_id>', post_update, name='update_post'),
    path('post/bloger/<uuid:pk>', BlogerPostView.as_view(), name='bloger_post'),





  
]
