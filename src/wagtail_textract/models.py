from django.db import models
from wagtail.documents.models import Document


class Document(Document):
    """Extra fields and methods for Document model."""
    transcription = models.TextField(null=True)

    def transcribe(self):
        """Extract text from file."""
        pass
