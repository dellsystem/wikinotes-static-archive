python=/usr/bin/env python

all: clean build

build:
	mkdir -p docs
	mkdir -p docs/static
	$(python) manage.py distill-local --force docs
	$(python) manage.py collectstatic --noinput

clean:
	rm -rf docs
