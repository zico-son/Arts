from django.apps import AppConfig


class ProjectshubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ProjectsHub'

    def ready(self):
        import ProjectsHub.signals
