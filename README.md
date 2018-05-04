# Text extraction for Wagtail document search

This package is for replacing [Wagtail][1]'s Document class with one
that allows searching in Document file contents using [textract][2].

Textract can extract text from (among [others][6]) PDF, Excel and Word files.

The package was inspired by the ["Search: Extract text from documents" issue][3] in Wagtail.

Documents will work as before, except that Document search in Wagtail's admin interface
will also find search terms in the files' contents.

The assumption is that this search should not only be available in Wagtail's admin interface,
but also in a public-facing search view, for which we provide a code example.


## Requirements

- Wagtail 2
- Tested on Python 3.4, 3.5 and 3.6
- The [Textract dependencies][8]


## Installation

- Install the [Textract dependencies][8]
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

Transcription is done automatically after Document save,
in an [`asyncio`][7] executor to prevent blocking the response during processing.

This is done using a new `document_saved` signal,
which is emitted by the new Document model's object on every save.

To transcribe all existing Documents, run the management command::

    ./manage.py transcribe_documents

This may take a long time, obviously.


## Usage in custom view

Here is a code example for a search view (outside Wagtail's admin interface)
that shows both Page and Document results.

```python
from itertools import chain

from wagtail.core.models import Page
from wagtail.documents.models import get_document_model


def search(request):
    # Search
    search_query = request.GET.get('query', None)
    if search_query:
        page_results = Page.objects.live().search(search_query)
        document_results = Document.objects.search(search_query)
        search_results = list(chain(page_results, document_results))

        # Log the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.none()

    # Render template
    return render(request, 'website/search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
```

Your template should allow for handling Documents differently than Pages,
because you can't do `pageurl result` on a Document:

```jinja2
{% if result.file %}
   <a href="{{ result.url }}">{{ result }}</a>
{% else %}
   <a href="{% pageurl result %}">{{ result }}</a>
{% endif %}
```


## Tests

To run tests, checkout this repository and:

    virtualenv --python=`which python3.6` env
    . env/bin/activate
    pip install -e ".[test]"
    pytest


## TO DO

- Check textract dependency version compatibility with current Wagtail dependencies


## Contributors

- Karl Hobley
- Bertrand Bordage
- Kees Hink
- Tom Hendrikx
- Coen van der Kamp
- Mike Overkamp
- Thibaud Colas


[1]: https://wagtail.io/
[2]: https://github.com/deanmalmgren/textract
[3]: https://github.com/wagtail/wagtail/issues/542
[4]: https://github.com/tesseract-ocr
[5]: https://github.com/tesseract-ocr/tessdata
[6]: http://textract.readthedocs.io/en/stable/#currently-supporting
[7]: https://docs.python.org/3/library/asyncio.html
[8]: http://textract.readthedocs.io/en/latest/installation.html
