#!/bin/bash

function up {
    exec docker-compose up -d
}

function setup {
    exec docker-compose up -d --build
    exec docker-compose exec web ./manage.py createsuperuser
}

function stop {
    exec docker-compose stop
}

function clean {
    exec docker-compose down
    exec docker-compose rm -a
}
