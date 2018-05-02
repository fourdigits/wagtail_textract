from django.apps import AppConfig


class WagtailTextractAppConfig(AppConfig):
    """Wagtail-Textract AppConfig."""
    name = 'wagtail_textract'
    label = 'wagtail_textract'
    verbose_name = "Wagtail-Textract Search integration"

    def ready(self):
        """Register signal handlers after loading."""
        from wagtail_textract.signal_handlers import register_signal_handlers
        register_signal_handlers()
