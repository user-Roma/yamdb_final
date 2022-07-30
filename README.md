# "YaMDb"
## Description
This is a RESTful API for "YaMDb", a rating service for artworks like movies, books or songs.
## Technology
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
![example workflow](https://github.com/user-Roma/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## .env template
``` 
DB_ENGINE=foo
DB_NAME=fooo
POSTGRES_USER=fooo
POSTGRES_PASSWORD=foooo
DB_HOST=db
DB_PORT=5432
DJANGO_SECRET_KEY='foooo'
DJANGO_ALLOWED_HOSTS=*
``` 
## How to run the project in dev-mode
- clone this repository to your local machine
```
git clone https://github.com/SokolovskiR/api_yamdb
``` 
- create a virtual environment
```
python3 m -venv venv
``` 
- activate virtual environment
```
source venv/bin/activate
``` 
- install dependencies in requirements.txt
```
pip install -r requirements.txt
``` 
- inside the folder with manage.py file execute the following command for migrations:
```
python3 manage.py migrate
```
- inside the same folder execute this command to create a superuser:
```
python3 manage.py createsuperuser
```
- inside the same folder execute this command to start the development server:
```
python3 manage.py runserver
```
## Command description for launching applications in Docker-compose
- run docker
```
sudo systemctl start docker
```
- create and start containers from the directory ../infra_sp2/infra/
```
sudo docker-compose up --build
```
## Commands for filling the database, run from the directory ../infra_sp2/infra/
- run migrations 
```
sudo docker-compose exec web python manage.py makemigrations
```
```
sudo docker-compose exec web python manage.py migrate
```
- collect the static files
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
- OPTIONAL: copy test data
```
sudo docker cp fixtures.json 5e7c14dfa40e:app/fixtures.json
```
- OPTIONAL: load data test data
```
sudo docker-compose exec web python manage.py loaddata fixtures.json
```
- create superuser
```
sudo docker-compose exec web python manage.py createsuperuser
```
## REST API available endpoints

After you started the development server, go to */api/v1/redoc/* URL where you can find the API documentation with available endpoints.

### Authors
RomanS, AlexanderK, RomanY