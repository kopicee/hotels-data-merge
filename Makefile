all: install

install:  ## Install dependencies locally
	pipenv install

run:  ## Run app locally
	pipenv run app

test:  ## Run tests locally
	pipenv run tests

do-build:  ## Build docker image
	sudo docker build . -t hotelsdatamerge:local

do-run: do-build  ## Run app using docker image
	sudo docker run -it --rm -p 8000:8000 hotelsdatamerge:local run app

do-test: do-build  ## Run tests using docker image
	sudo docker run -it --rm hotelsdatamerge:local run tests

help:  ## Show this help
	@echo 'usage: make [target] ...'
	@echo
	@egrep '^(.+)\:\ .*##\ (.+)' ${MAKEFILE_LIST} | sed 's/:.*##/#/' | column -t -c 2 -s '#'
