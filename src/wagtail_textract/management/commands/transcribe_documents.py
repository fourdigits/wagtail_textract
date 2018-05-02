from django.core.management.base import BaseCommand

from wagtail.documents.models import get_document_model


class Command(BaseCommand):
    """Extract text from all Documents."""

    def handle(self, *args, **options):
        """Extract text from all Documents."""
        for document in get_document_model().objects.all():
            self.stdout.write("Transcribing %s" % document)
            document.transcribe()
