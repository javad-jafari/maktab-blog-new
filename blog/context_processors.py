from blog.models import Category
from django.utils import timezone



def show_category(request):
    return {
        "categories":Category.objects.all(),
        "time":timezone.now()
        }