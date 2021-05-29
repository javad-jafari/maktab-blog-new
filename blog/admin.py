from django.contrib import admin

from .models import Post, Category, Comment, PostSetting, CommentLike


# Register your models here.







from mptt.admin import DraggableMPTTAdmin



class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_posts_count', 'related_posts_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Post,
                'category',
                'posts_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Post,
                 'category',
                 'posts_count',
                 cumulative=False)
        return qs

    def related_posts_count(self, instance):
        return instance.posts_count
    related_posts_count.short_description = 'Related posts (for this specific category)'

    def related_posts_cumulative_count(self, instance):
        return instance.posts_cumulative_count
    related_posts_cumulative_count.short_description = 'Related posts (in tree)'
























# ---------------------------------------------------------------------------------------------
# class ChildrenItemInline(admin.TabularInline):
#     model = Category
#     fields = (
#         'title', 'slug'
#     )
#     extra = 1
#     show_change_link = True


# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('slug', 'title', 'parent')
#     search_fields = ('slug', 'title')
#     list_filter = ('parent',)
#     inlines = [
#         ChildrenItemInline,
#     ]


class PostSettingInline(admin.TabularInline):
    model = PostSetting


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at', 'update_at',
                    'publish_time', 'draft','promote', 'category', 'author','seen')
    search_fields = ('title',)
    list_filter = ('draft', 'category', 'author')
    date_hierarchy = 'publish_time'
    list_editable = ('draft',)
    inlines = (PostSettingInline,)

    def make_published(self, request, queryset):
        queryset.update(draft=False)

    make_published.short_description = "Exit selected post from draft"

    # def allow_discoution(self, request, queryset):
    #     queryset.update(post_setting__allow_discusstion=True)
    # allow_discoution.short_description = "allow user write comment on posts"

    actions = [make_published]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'is_confirmed', 'author',
                    'like_count', 'dislike_count')
    search_fields = ('content',)
    list_filter = ('is_confirmed',)
    date_hierarchy = 'create_at'


admin.site.register(Category, CategoryAdmin)
admin.site.register(CommentLike)
