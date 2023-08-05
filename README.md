# hotels-data-merge

[![Tests](https://github.com/kopicee/hotels-data-merge/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/kopicee/hotels-data-merge/actions/workflows/ci.yml)


## Build, test and run

Locally:
```sh
# Install pipenv
pip install pipenv

# Install dependencies in an isolated virtual environment:
pipenv shell
pipenv install

# Run tests and start app
pipenv run tests
pipenv run app
```

Using Docker:
```sh
# Build image
docker build . -t hotelsdatamerge:local

# Run tests
docker run -it --rm hotelsdatamerge:local run tests

# Start app
docker run -it --rm -p 8000:8000 hotelsdatamerge:local run app
```


## Usage

- Open the app at http://127.0.0.1:8000 to see the interactive Swagger API docs.


## Modified response format

- Added pagination support (simple offset/limit approach)
