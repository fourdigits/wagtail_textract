from wagtail.documents.models import get_document_model


def test_document_class():
    """Test that the Document model has the required (search) field.

    Actually, this only tests if Wagtails WAGTAILDOCS_DOCUMENT_MODEL
    still works, and that our test Django settings are correct.
    """
    Document = get_document_model()
    assert hasattr(Document, 'transcription')
    assert 'transcription' in [f.field_name for f in Document.search_fields]
