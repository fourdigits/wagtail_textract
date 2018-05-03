import logging
import textract

from wagtail.documents.models import get_document_model

from wagtail_textract.signals import document_saved

logger = logging.getLogger(__name__)


def transcribe_document(instance, **kwargs):
    """Store the Document file's text in the transcription field."""
    try:
        text = textract.process(instance.file.path).strip()
        if not text:
            logger.debug('No text found, falling back to tesseract.')
            text = textract.process(
                instance.file.path,
                method='tesseract',
            ).strip()

    except Exception as err:
        text = None
        logger.error(
            'Text extraction error with file {file}: {message}'.format(
                file=instance.filename,
                message=str(err),
            )
        )

    if text:
        instance.transcription = text.decode()
        instance.save(document_saved_signal=False)
        print("Saved transcription: %s" % text)
    else:
        logger.error('No text found.')


def register_signal_handlers():
    """Transcribe Document on save."""
    Document = get_document_model()

    document_saved.connect(transcribe_document, sender=Document)
