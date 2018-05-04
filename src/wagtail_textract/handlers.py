import asyncio
import logging
import textract

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()


def transcribe_document(document):
    """Store the Document file's text in the transcription field."""
    try:
        text = textract.process(document.file.path).strip()
        if not text:
            logger.debug('No text found, falling back to tesseract.')
            text = textract.process(
                document.file.path,
                method='tesseract',
            ).strip()

    except Exception as err:
        text = None
        logger.error(
            'Text extraction error with file {file}: {message}'.format(
                file=document.filename,
                message=str(err),
            )
        )

    if text:
        document.transcription = text.decode()
        document.save(transcribe=False)
        print("Saved transcription: %s" % text)
    else:
        logger.error('No text found.')


def async_transcribe_document(document):
    """Defer transcription to an asyncio executor."""
    loop.run_in_executor(None, transcribe_document, document)
