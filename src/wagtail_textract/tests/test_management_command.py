import pytest
import time

from django.core.files import File
from django.core.management import call_command
from wagtail.documents.models import get_document_model

Document = get_document_model()


@pytest.mark.django_db
def test_management_command():
    """Test the transcribe_documents management script.

    This creates a Document with the file `test_document.pdf`, which contains
    the hand-written words "CORRECT HORSE BATTERY STAPLE" on separate lines.
    Unfortunately, the handwriting is not clear enough so OCR recognizes
    'CORRECT H o R SEâ€™ BATTE Ry STAPLE'
    """
    path = './src/wagtail_textract/tests/testfiles/'
    fhandle = open('%s/test_document.pdf' % path, 'rb')
    file = File(fhandle)
    document = Document.objects.create(
        title="Test file",
        file=file,
    )
    fhandle.close()
    document.save()
    call_command('transcribe_documents')

    # Transcription field is empty initially
    document.refresh_from_db()
    assert document.transcription == ''

    # After some time, transcription is complete
    time.sleep(10)
    document.refresh_from_db()
    assert 'CORRECT' not in document.transcription
    assert 'STAPLE' not in document.transcription
