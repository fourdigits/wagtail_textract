ENV = env
PYTHON_VERSION = 3.9
PYTHON = $(ENV)/bin/python$(PYTHON_VERSION)

$(ENV):
	$(shell which python$(PYTHON_VERSION)) -m venv $(ENV)
	$(PYTHON) -m pip install --upgrade pip setuptools wheel

tessdata:
	mkdir tessdata
	cd tessdata && curl -LJO https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata

test: tessdata env
	$(PYTHON) -m pip install -e '.[test]'
	$(ENV)/bin/coverage run $(ENV)/bin/pytest
