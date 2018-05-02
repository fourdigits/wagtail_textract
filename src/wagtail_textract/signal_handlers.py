from wagtail.documents.models import get_document_model

from wagtail_textract.signals import document_saved


def transcribe_document(instance, **kwargs):
    """Call the Document's transcribe method."""
    instance.transcribe()


def register_signal_handlers():
    """Transcribe Document on save."""
    Document = get_document_model()

    document_saved.connect(transcribe_document, sender=Document)
