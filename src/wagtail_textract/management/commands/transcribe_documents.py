from django.core.management.base import BaseCommand

try:
    from wagtail.documents.models import get_document_model # wagtail < 2.8
except ImportError:
    from wagtail.documents import get_document_model # wagtail >= 2.8

from wagtail_textract.handlers import async_transcribe_document


class Command(BaseCommand):
    """Extract text from all Documents."""

    def handle(self, *args, **options):
        """Extract text from all Documents."""
        for document in get_document_model().objects.all():
            self.stdout.write("Transcribing %s" % document)
            async_transcribe_document(document)
