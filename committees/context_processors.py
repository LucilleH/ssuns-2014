from committees.models import Category

# There isn't really a better way of doing this, I'm sorry
def committees(request):
    return {
        'categories': Category.objects.all()
    }
