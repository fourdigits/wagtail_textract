import pkg_resources

__version__ = pkg_resources.get_distribution("wagtail_textract").version

default_app_config = 'wagtail_textract.apps.WagtailTextractAppConfig'
