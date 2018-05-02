# Text extraction for Wagtail document search

This package is for replacing [Wagtail][1]'s Document class with one
that allows searching in Document file contents using [textract][2].

The package was inspired by the ["Search: Extract text from documents" issue][3] in Wagtail.

## Installation

- Install the Texttract dependencies: http://textract.readthedocs.io/en/latest/installation.html
- Add `wagtail_textract` to your requirements and/or `pip install wagtail_textract`
- Add to your Django `INSTALLED_APPS`, after `wagtail.documents`.
- Put `WAGTAILDOCS_DOCUMENT_MODEL = "wagtail_textract.document"` in your Django settings.


## Transcribing

Transcribing is done automatically on Document save.

This is done using a new `document_saved` signal,
which is emitted by the new Document model's object on every save.

To transcribe all existing Documents, run the management command::

    ./manage.py transcribe_documents

This may take a long time, obviously.


[1]: https://wagtail.io/
[2]: https://github.com/deanmalmgren/textract
[3]: https://github.com/wagtail/wagtail/issues/542
