python=/usr/bin/env python

all: clean build

build:
	mkdir -p public
	mkdir -p public/static
	$(python) manage.py collectstatic --noinput
	$(python) manage.py distill-local --force public

clean:
	rm -rf public
