from wagtail.tests.settings import *

MEDIA_ROOT = '.'
WAGTAILDOCS_DOCUMENT_MODEL = 'wagtail_textract.document'
INSTALLED_APPS = INSTALLED_APPS + ('wagtail_textract',)
