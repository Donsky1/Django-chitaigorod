from django import template

register = template.Library()


@register.filter(name='status_user')
def status_user(user):
    if not user.is_authenticated:
        return 'anonymous'
    else:
        if user.is_superuser:
            return user.username.upper() + 'superuser'
        else:
            return user.username.upper() + 'user'
