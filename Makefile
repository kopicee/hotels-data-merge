all: install

install:
	pipenv install

run:
	python3 src/main.py

test:
	pytest
