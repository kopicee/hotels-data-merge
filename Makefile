all: install

install:
	pipenv install

run:
	pipenv run app

test:
	pipenv run tests

do-build:
	sudo docker build . -t hotelsdatamerge:local

do-run:
	sudo docker run -it --rm -p 8000:8000 hotelsdatamerge:local run app

do-test:
	sudo docker run -it --rm hotelsdatamerge:local run tests
