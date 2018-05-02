import logging
import textract

from django.db import models
from wagtail.documents.models import Document as WagtailDocument
from wagtail.search import index

from .signals import document_saved

logger = logging.getLogger(__name__)


class Document(WagtailDocument):
    """Extra fields and methods for Document model."""
    transcription = models.TextField(default='')
    search_fields = WagtailDocument.search_fields + [
        index.SearchField(
            'transcription',
            partial_match=False,
        ),
    ]

    def transcribe(self):
        """Extract text from file."""
        try:
            text = textract.process(self.file.path).strip()
            if not text:
                logger.debug('No text found, falling back to tesseract.')
                text = textract.process(
                    self.file.path,
                    method='tesseract',
                ).strip()

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
            self.save(document_saved_signal=False)
            print("Saved transcription: %s" % text)
        else:
            logger.error('No text found.')

    def save(self, **kwargs):
        """Send the document_saved signal."""
        send_signal = kwargs.pop('document_saved_signal', True)
        super(Document, self).save(**kwargs)
        if send_signal:
            document_saved.send(sender=self.__class__, instance=self)
