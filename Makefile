env:
	virtualenv --python=`which python3` env

tessdata:
	mkdir tessdata
	cd tessdata && curl -LJO https://github.com/tesseract-ocr/tessdata/raw/master/eng.traineddata

test: tessdata env
	env/bin/pip install -e ".[test]"
	coverage run env/bin/pytest
