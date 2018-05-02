import logging
import textract

from django.db import models
from wagtail.documents.models import Document

logger = logging.getLogger(__name__)


class Document(Document):
    """Extra fields and methods for Document model."""
    transcription = models.TextField(null=True)

    def transcribe(self):
        """Extract text from file."""
        try:
            text = textract.process(self.file.path)
        except Exception as err:
            text = None
            logger.error(
                'Text extraction error with file {file}: {message}'.format(
                    file=self.filename,
                    message=str(err),
                )
            )

        if text:
            self.transcription = text.decode()
            self.save()
            logger.info("Saved transcription: %s" % text)
