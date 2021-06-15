from blog.models import Category,Comment,RequestAuthor
from django.utils import timezone
from jalali_date import datetime2jalali, date2jalali


def show_category(request):
    return {
        "categories":Category.objects.all(),
        "time":datetime2jalali(timezone.now()).strftime('%y/%m/%d _ %H:%M:%S'),
        "not_confirmed_comment":Comment.objects.filter(is_confirmed=False),
        "req_author":RequestAuthor.objects.filter(confirm=False)
        }