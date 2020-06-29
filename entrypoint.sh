#!/bin/sh

pipenv run flask db upgrade
pipenv run waitress-serve --call 'app:create_app'
