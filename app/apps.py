from django.apps import AppConfig


class AtalanteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    # Keep the historical label so committed migrations and table names still resolve.
    label = 'web_dashboard'
