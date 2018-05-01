TODO
====

Incompatible versions
---------------------

Installation in a Wagtail 2.0.1 virtualenv yields::

    requests 2.18.4 has requirement chardet<3.1.0,>=3.0.2, but you'll have chardet 2.3.0 which is incompatible.
    textract 1.6.1 has requirement beautifulsoup4==4.5.3, but you'll have beautifulsoup4 4.6.0 which is incompatible.


Migration location
------------------

Running migrations yields::

    $ ./manage.py makemigrations
    wagtail_textract patching Document model
    Migrations for 'wagtaildocs':
      env/lib/python3.6/site-packages/wagtail/documents/migrations/0008_document_extracted_text.py
        - Add field extracted_text to document

This is not the right place for migrations.
