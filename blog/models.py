from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify





class Category(MPTTModel):
    title = models.CharField(_("Title"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True, db_index=True, allow_unicode=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['title']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.slug


class Post(models.Model):
    title = models.CharField(_("Title"), max_length=128)
    promote = models.BooleanField(_('promote'), default=False)
    abstract = models.CharField(_("Abstract"), max_length=130, default='none')
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    content = RichTextField(_("Content"), blank=True, null=True)
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    publish_time = models.DateTimeField(_("Publish at"), db_index=True)
    draft = models.BooleanField(_("Draft"), default=True, db_index=True)
    image = models.ImageField(_("image"), upload_to='post/images')
    category = models.ForeignKey(Category, related_name='posts', verbose_name=_(
        "Category"), on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"),
                               related_name='posts', related_query_name='children',
                               on_delete=models.SET_NULL, null=True, blank=True)
    seen = models.PositiveIntegerField(_("seen"),default=0)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-publish_time']

    def __str__(self):
        return self.title
        
    def incrementViewCount(self):
        self.seen += 1
        self.save()
        return self.seen

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)


class PostSetting(models.Model):
    post = models.OneToOneField(
        "Post", verbose_name=_("post"), related_name='post_setting', related_query_name='post_setting',
        on_delete=models.CASCADE)
    comment = models.BooleanField(_("comment"))
    author = models.BooleanField(_("author"))
    allow_discussion = models.BooleanField(_("allow discussion"))

    class Meta:
        verbose_name = _("PostSetting")
        verbose_name_plural = _("PostSettings")


class CommentLike(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    comment = models.ForeignKey('blog.Comment', verbose_name=_(
        'Comment'), related_name='comment_like', related_query_name='comment_like', on_delete=models.CASCADE)
    condition = models.BooleanField(_("Condition"))
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)

    class Meta:
        unique_together = [['author', 'comment']]
        verbose_name = _("CommentLike")
        verbose_name_plural = _("CommentLikes")

    def __str__(self):
        return str(self.condition)


class Comment(models.Model):
    content = models.TextField(_("Content"))
    post = models.ForeignKey(Post, related_name='comments', related_query_name='comments', verbose_name=_(
        "Post"), on_delete=models.CASCADE)
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(_("confirm"), default=False)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-create_at']

    def __str__(self):
        return self.post.title

    @property
    def like_count(self):
        q = CommentLike.objects.filter(comment=self, condition=True)
        return q.count()

    @property
    def dislike_count(self):
        q = self.comment_like.filter(condition=False)
        return q.count()


class RequestAuthor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(
        "Author_req"),related_query_name='req_author',related_name='req_author', on_delete=models.CASCADE)
    confirm = models.BooleanField(_('confirm req_author'),default=False)
    def __str__(self):
        return self.user.email