import asyncio
import logging
import textract

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()


def transcribe_document(document, options):
    """Store the Document file's text in the transcription field."""
    try:
        text = textract.process(document.file.path).strip()
        if not text:
            if 'verbosity' in options and options['verbosity'] >= 2:
                print('No text found - falling back to tesseract:  {} ({})'.format(document, document.filename))
            text = textract.process(
                document.file.path,
                method='tesseract',
            ).strip()

    except Exception as err:
        text = None
        logger.error(
            '\n\nText extraction error with file {file}:  {message}\n\n'.format(
                file=document.filename,
                message=str(err),
            )
        )

    if text:
        document.transcription = text.decode()
        document.save(transcribe=False)
        if 'verbosity' in options and options['verbosity'] == 3:
            print("Saved transcription for {}:\n{}\n".format(document, text))
    else:
        logger.error('No text found:  {} ({})'.format(document, document.filename))


def async_transcribe_document(document, options):
    """Defer transcription to an asyncio executor."""
    loop.run_in_executor(None, transcribe_document, document, options)

