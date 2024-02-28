from manage_category.models import Category


def category_nav(request):
    category = Category.objects.filter(is_listed = True)
    return { 'cat' : category}