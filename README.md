[![Build Status](https://travis-ci.org/fourdigits/wagtail_textract.svg?branch=master)](https://travis-ci.org/fourdigits/wagtail_textract)
[![Coverage Report](http://codecov.io/github/fourdigits/wagtail_textract/coverage.svg?branch=master)](http://codecov.io/github/fourdigits/wagtail_textract?branch=master)

# Text extraction for Wagtail document search

This package is for replacing [Wagtail][1]'s Document class with one
that allows searching in Document file contents using [textract][2].

Textract can extract text from (among [others][6]) PDF, Excel and Word files.

The package was inspired by the ["Search: Extract text from documents" issue][3] in Wagtail.

Documents will work as before, except that Document search in Wagtail's admin interface
will also find search terms in the files' contents.

Some screenshots to illustrate.

In our fresh Wagtail site with `wagtail_textract` installed,
we uploaded a [file called `test_document.pdf`](./src/wagtail_textract/tests/testfiles/test_document.pdf) with handwritten text in it.
It is listed in the admin interface under Documents:

![Document List](/docs/screenshot_document_list_test_document.png)

If we now search in Documents for the word `correct`, which is one of the handwritten words,
the live search finds it:

![Document Search finds PDF by searching for "staple"](/docs/screenshot_document_search_correct.png)

The assumption is that this search should not only be available in Wagtail's admin interface,
but also in a public-facing search view, for which we provide a code example.


## Requirements

- Wagtail 2 (see [tox.ini](./tox.ini))
- The [Textract dependencies][8]


## Maturity

We have been using this package in production since August 2018 on https://nuffic.nl.


## Installation

- Install the [Textract dependencies][8]
- Add `wagtail_textract` to your requirements and/or `pip install wagtail_textract`
- Add to your Django `INSTALLED_APPS`.
- Put `WAGTAILDOCS_DOCUMENT_MODEL = "wagtail_textract.document"` in your Django settings.

Note: You'll get an incompatibility warning during installation of wagtail_textract (Wagtail 2.0.1 installed):

```
requests 2.18.4 has requirement chardet<3.1.0,>=3.0.2, but you'll have chardet 2.3.0 which is incompatible.
textract 1.6.1 has requirement beautifulsoup4==4.5.3, but you'll have beautifulsoup4 4.6.0 which is incompatible.
```

We haven't seen this leading to problems, but it's something to keep in mind.


### Tesseract

In order to make `textract` use [Tesseract][4], which happens if regular
`textract` finds no text, you need to add the data files that Tesseract can
base its word matching on.

Create a `tessdata` directory in your project directory, and download the
[languages][5] you want.


## Transcribing

Transcription is done automatically after Document save,
in an [`asyncio`][7] executor to prevent blocking the response during processing.

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


## What if you already use a custom Document model?

In order to use wagtail_textract, your `CustomizedDocument` model should do
the same as [wagtail_textract's Document](./src/wagtail_textract/models.py):

- subclass `TranscriptionMixin`
- alter `search_fields`

```python
from wagtail_textract.models import TranscriptionMixin


class CustomizedDocument(TranscriptionMixin, ...):
    """Extra fields and methods for Document model."""
    search_fields = ... + [
        index.SearchField(
            'transcription',
            partial_match=False,
        ),
    ]
```

Note that the first class to subclass should be `TranscriptionMixin`,
so its `save()` takes precedence over that of the other parent classes.


## Tests

To run tests, checkout this repository and:

    make test


### Coverage

A coverage report will be generated in `./coverage_html_report/`.


## Contributors

- Karl Hobley
- Bertrand Bordage
- Kees Hink
- Tom Hendrikx
- Coen van der Kamp
- Mike Overkamp
- Thibaud Colas
- Dan Braghis


[1]: https://wagtail.io/
[2]: https://github.com/deanmalmgren/textract
[3]: https://github.com/wagtail/wagtail/issues/542
[4]: https://github.com/tesseract-ocr
[5]: https://github.com/tesseract-ocr/tessdata
[6]: http://textract.readthedocs.io/en/stable/#currently-supporting
[7]: https://docs.python.org/3/library/asyncio.html
[8]: http://textract.readthedocs.io/en/latest/installation.html
