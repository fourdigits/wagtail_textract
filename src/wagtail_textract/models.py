from django.db import models
from wagtail.documents.models import Document

from .patch_model import patch_model


class DocumentOverride(object):
    """Extra fields and methods for Document model."""
    transcription = models.TextField(null=True)

    def transcribe(self):
        """Extract text from file."""
        pass


patch_model(Document, DocumentOverride)
