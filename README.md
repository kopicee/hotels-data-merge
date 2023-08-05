# hotels-data-merge

[![Tests](https://github.com/kopicee/hotels-data-merge/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/kopicee/hotels-data-merge/actions/workflows/ci.yml)


## Usage

Install pipenv:
```sh
pip install pipenv
```

Create a self-contained virtual environment to isolate dependencies, then install dependencies:
```sh
pipenv shell
pipenv install
```

Run tests and start app:
```sh
pipenv run tests
pipenv run app
```

Open the app at http://127.0.0.1:8000 to see the interactive Swagger API docs.


## Modified response format

- Added pagination support (simple offset/limit approach)
