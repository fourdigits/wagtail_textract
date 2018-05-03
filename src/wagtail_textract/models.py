from django.db import models
from wagtail.documents.models import Document as WagtailDocument
from wagtail.search import index

from .signals import document_saved


class TranscriptionMixin(models.Model):
    """Mixin class with transcription field."""
    transcription = models.TextField(default='', blank=True)

    class Meta:
        """Don't create a table, this model is only for subclassing."""
        abstract = True


class Document(WagtailDocument, TranscriptionMixin):
    """Extra fields and methods for Document model."""
    search_fields = WagtailDocument.search_fields + [
        index.SearchField(
            'transcription',
            partial_match=False,
        ),
    ]

    def save(self, **kwargs):
        """Send the document_saved signal."""
        send_signal = kwargs.pop('document_saved_signal', True)
        super(Document, self).save(**kwargs)
        if send_signal:
            document_saved.send(sender=self.__class__, instance=self)
