from django.apps import AppConfig


class LoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'
    # include signal to handle user login
    def ready(self):
        import login.signals