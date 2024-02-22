python=/usr/bin/env python

all: clean build

build:
	mkdir -p public
	mkdir -p public/static
	$(python) manage.py distill-local --force public
	$(python) manage.py collectstatic --noinput

clean:
	rm -rf public
