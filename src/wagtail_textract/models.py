from django.db import models
from wagtail.documents.models import Document as WagtailDocument
from wagtail.search import index

from wagtail_textract.handlers import async_transcribe_document


class TranscriptionMixin(models.Model):
    """Mixin class with transcription field and save method."""
    transcription = models.TextField(default='', blank=True)

    class Meta:
        """Don't create a table, this model is only for subclassing."""
        abstract = True

    def save(self, **kwargs):
        """Asynchronously transcribe the file."""
        transcribe = kwargs.pop('transcribe', True)
        super(TranscriptionMixin, self).save(**kwargs)
        if transcribe:
            async_transcribe_document(self)


class Document(TranscriptionMixin, WagtailDocument):
    """Include transcription in search_fields."""
    search_fields = WagtailDocument.search_fields + [
        index.SearchField(
            'transcription',
            partial_match=False,
        ),
    ]
