Text extraction for Wagtail document search
===========================================

https://github.com/wagtail/wagtail/issues/542

Installation
------------

- Install the Texttract dependencies: http://textract.readthedocs.io/en/latest/installation.html
- Add `wagtail_textract` to your requirements and/or `pip install wagtail_textract`
- Add to your Django `INSTALLED_APPS`, after `wagtail.documents`.
- Put `WAGTAILDOCS_DOCUMENT_MODEL = "wagtail_textract.document"` in your Django settings.


Transcribing
------------

Run the management command::

    ./manage.py transcribe_documents
