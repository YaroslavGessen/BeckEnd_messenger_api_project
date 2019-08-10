from django.apps import AppConfig


class MessangerConfig(AppConfig):
    name = 'messanger'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import messanger.signals