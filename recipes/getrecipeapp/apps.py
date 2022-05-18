from django.apps import AppConfig


class GetrecipeappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'getrecipeapp'

    def ready(self):
        from . import signals