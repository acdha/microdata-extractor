FROM python:3.7

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update -qqy && apt-get dist-upgrade -qqy -o Dpkg::Options::='--force-confnew' && apt-get -qqy autoremove && apt-get -qqy autoclean

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

RUN pip install --quiet --upgrade pip
RUN pip install --quiet --upgrade pipenv

WORKDIR /app
COPY . /app

RUN pipenv install --system --deploy

EXPOSE 80

CMD gunicorn --preload --bind 0.0.0.0:80 microdata_extractor.wsgi:application
