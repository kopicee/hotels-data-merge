all: install

install:
	pipenv install

run:
	pipenv run app

test:
	pipenv run tests
