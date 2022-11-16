from django.apps import AppConfig


class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pharmacyPage'

    # add this
    def ready(self):
        import pharmacyPage.signals  # noqa