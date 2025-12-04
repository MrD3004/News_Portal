from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    """
    App configuration for the 'articles' app.
    Ensures signal handlers are registered when the app is ready.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "articles"

    def ready(self):
        # Explicitly import signal handlers to ensure they are connected
        import articles.signals  # noqa: F401
