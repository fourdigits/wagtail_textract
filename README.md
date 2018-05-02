# Text extraction for Wagtail document search

This package is for replacing [Wagtail][1]'s Document class with one
that allows searching in Document file contents using [textract][2].

The package was inspired by the ["Search: Extract text from documents" issue][3] in Wagtail.

## Installation

- Install the Texttract dependencies: http://textract.readthedocs.io/en/latest/installation.html
- Add `wagtail_textract` to your requirements and/or `pip install wagtail_textract`
- Add to your Django `INSTALLED_APPS`, after `wagtail.documents`.
- Put `WAGTAILDOCS_DOCUMENT_MODEL = "wagtail_textract.document"` in your Django settings.


### Tesseract

In order to make `textract` use [Tesseract][4], which happens if regular
`textract` finds no text, you need to add the data files that Tesseract can
base its word matching on.

Create a `tessdata` directory in your project directory, and download the
[languages][5] you want.


## Transcribing

Transcribing is done automatically on Document save.

This is done using a new `document_saved` signal,
which is emitted by the new Document model's object on every save.

To transcribe all existing Documents, run the management command::

    ./manage.py transcribe_documents

This may take a long time, obviously.


## TO DO

- Check textract dependency version compatibility with current Wagtail dependencies
- Handle `transcribe()` asynchronously or in a cron job, to prevent long waits on upload / edit

[1]: https://wagtail.io/
[2]: https://github.com/deanmalmgren/textract
[3]: https://github.com/wagtail/wagtail/issues/542
[4]: https://github.com/tesseract-ocr
[5]: https://github.com/tesseract-ocr/tessdata
