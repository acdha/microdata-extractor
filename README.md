# HTML5 Microdata Extractor

This is the bare minimum needed to expose https://github.com/edsu/microdata as a
running web service

## Local operations

1. `pipenv install`
1. `pipenv run gunicorn microdata_extractor.wsgi:application`

## Deployment

### Docker

1. `docker build -t microdata-extractor .`
1. Run the container mapping port 80 to somewhere useful: e.g. `docker run --rm -p 80:80 -i microdata-extractor`

### Deployment on OpenShift

1. Enable Pipenv in the build environment: `oc set env bc/microdata-extractor ENABLE_PIPENV=1`
1. Start a build if necessary: `oc start-build microdata-extractor -n microdata-extractor`
