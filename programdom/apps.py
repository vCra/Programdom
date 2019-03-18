from django.apps import AppConfig


class ProgramdomConfig(AppConfig):
    name = 'programdom'
    verbose_name = "Programdom"

    def ready(self):
        from . import signals
