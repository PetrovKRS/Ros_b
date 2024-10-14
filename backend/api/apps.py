from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        # Импортируем сигналы, чтобы они начали работать при старте приложения
        import api.signals  # noqa
