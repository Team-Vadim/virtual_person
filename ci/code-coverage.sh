#!/bin/bash

# run pylint
cd website/
coverage run manage.py test

mkdir public
coverage-badge -o public/coverage.svg

exit 0
