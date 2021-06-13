from account.views import get_author_req
from django.urls import path, re_path
from .views import (LogoutView, RegisterView,SignView, admin_add_category, admin_all_req_to_author,
					admin_comment_confirm, admin_comment_del, admin_confirm_to_author, admin_user_del,
					admin_user_get_author, admin_user_get_ban,
					userprofile,change_password,
					ProfileUpdate,admin_all_users,admin_all_categories,
					admin_all_comments,delete_post,draft_post,publish_post,
					)

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
	path('profile/posts/delete/<int:post_id>',delete_post , name='delete_post'),
	path('profile/posts/draft/<int:post_id>',draft_post , name='draft_post'),
	path('profile/posts/publish/<int:post_id>',publish_post , name='publish_post'),

	path('password/', change_password, name='change_password'),
	path('profile/update/<uuid:pk>/',ProfileUpdate.as_view() , name='profile_update'),
	path('profile/get_author/<uuid:user_id>', get_author_req, name='get_author_req'),

	path('siteadmin/',admin_all_users , name='admin_users'),
	path('siteadmin/users/delete/<uuid:user_id>',admin_user_del , name='admin_users_del'),
	path('siteadmin/users/get_author/<uuid:user_id>',admin_user_get_author , name='admin_users_get_author'),
	path('siteadmin/users/get_ban/<uuid:user_id>',admin_user_get_ban , name='admin_users_get_ban'),

	path('siteadmin/category',admin_all_categories , name='admin_categories'),
	path('siteadmin/category/new',admin_add_category , name='admin_new_category_add'),
	path('siteadmin/category/delete/<int:cat_id>',admin_all_categories , name='admin_categories_del'),

	path('siteadmin/comment',admin_all_comments , name='admin_comments'),
	path('siteadmin/comment/delete/<int:comment_id>',admin_comment_del , name='admin_comment_del'),
	path('siteadmin/comment/confirm/<int:comment_id>/<str:status>',admin_comment_confirm , name='admin_comment_confirm'),

	path('siteadmin/requested_to_get_author',admin_all_req_to_author , name='admin_all_req_to_author'),
	path('siteadmin/requested_to_get_author/take_author/<uuid:user_id>',admin_confirm_to_author, name='admin_confirm_to_author'),


]
