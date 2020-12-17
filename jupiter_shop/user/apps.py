from django.apps import AppConfig
from django.db.models.signals import post_save


class UserConfig(AppConfig):
    name = 'user'

    def ready(self):

        import user.signals


