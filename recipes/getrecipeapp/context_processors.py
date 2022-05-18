from .models import Tag


def tag_list(request):
    return {'tag_list': Tag.objects.order_by('name')}
