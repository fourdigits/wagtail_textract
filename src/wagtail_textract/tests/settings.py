from wagtail.tests.settings import *

MEDIA_ROOT = '.'
WAGTAILDOCS_DOCUMENT_MODEL = 'wagtail_textract.document'
if type(INSTALLED_APPS) is list:
    INSTALLED_APPS = INSTALLED_APPS + ['wagtail_textract',]
else:
    INSTALLED_APPS = INSTALLED_APPS + ('wagtail_textract',)
