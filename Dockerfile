FROM python:3.7

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update -qy && apt-get dist-upgrade -qy -o Dpkg::Options::='--force-confnew' && apt-get -qy autoremove && apt-get -qy autoclean

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

RUN pip install --upgrade pip
RUN pip install --upgrade pipenv

WORKDIR /app
COPY . /app

RUN pipenv install --system --deploy

EXPOSE 80

CMD gunicorn --preload --bind 0.0.0.0:80 microdata_extractor.wsgi:application
