FROM python:3.10

RUN pip install pipenv

WORKDIR /etc/app

COPY Pipfile Pipfile.lock /etc/app/

RUN pipenv install

COPY . /etc/app/

EXPOSE 8000

CMD pipenv run app
