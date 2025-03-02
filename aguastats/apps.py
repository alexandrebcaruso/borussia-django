from django.apps import AppConfig

class AguastatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aguastats'

    def ready(self):
        import aguastats.signals