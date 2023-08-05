all: install

install:
	pipenv install

run:
	pipenv run app

test:
	pipenv run tests

do-run:
	sudo docker build . -t hotelsdatamerge:local
	sudo docker run -it --rm -p 8000:8000 hotelsdatamerge:local
