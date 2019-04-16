# HTML5 Microdata Extractor

This is the bare minimum needed to expose https://github.com/edsu/microdata as a
running web service

## Local operations

1. `pipenv install`
1. `pipenv run gunicorn microdata_extractor.wsgi:application`

## Deployment on OpenShift

1. Enable Pipenv in the build environment: `oc set env bc/microdata-extractor ENABLE_PIPENV=1`
1. Start a build if necessary: `oc start-build microdata-extractor -n microdata-extractor`
