from blog.models import Category

def show_category(request):
    return {"categories":Category.objects.all()}