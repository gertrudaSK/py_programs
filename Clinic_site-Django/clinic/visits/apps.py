from django.apps import AppConfig


class VisitsConfig(AppConfig):
    name = 'visits'

    def ready(self):
        from .signals import create_profile, save_profile

