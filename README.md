
![YamDB](https://github.com/IzmdI/yamdb_final/workflows/yamdb_workflow/badge.svg)

# YaMDB

The YaMDB collects reviews from users on different titles. Titles divide by categories and have one or more genres. Categories and genres lists can be expand by administrator. Each review contains text and rating from 1 to 10. Each Title assigned average from all reviews. New users can be registered only by administrator.
It is haven't frontend, only API functionality.

## Getting Started

You need [Docker](https://www.docker.com/) to run YaMDB. Just clone repository and run docker-compose.

### Installing

First, open a `.env.example` file, set environment variables, and save it as `.env` without ".example".
IMPORTANT: Make own password for database.

```
SECRET_KEY=somedjangosecretkey
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgrespass # make Your
DB_HOST=db
DB_PORT=5432
```

Start building the container in terminal.

```
docker-compose up
```

YaMDB will deployed through Gunicorn with PostgreSQL database on your localhost, port number is 8000.

```
localhost:8000
```

Create administrator user like in usual django-based projects. The most convenient way to do it directly inside the container.

```
docker exec -it <CONTAINER ID> bash
```

```
python manage.py createsuperuser
```

To out from container just do exit.

```
exit
```

Congratulations! Now You can manage YaMDB from admin page.

```
localhost:8000/admin
```

You can check, how it looks here:

```
http://130.193.34.222/
```

### Test data

If You want, You can download some test data from dump. Or You can create them from admin page by yourself.
IMPORTANT: Load data from dump need to do inside the container.

```
python3 manage.py shell  

>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()

python manage.py loaddata dump.json 
```

## Built With

* [Django 3.0](https://www.djangoproject.com/) - The web framework used
* [DRF 3.11](https://www.django-rest-framework.org/) - Django REST framework, powerfull API toolkit
* [DRF simple JWT 4.4](https://github.com/SimpleJWT/django-rest-framework-simplejwt) - JSON Web Token authentication plugin for the Django REST Framework
* [PostgreSQL 13.1](https://www.postgresql.org/) - Database
* [Gunicorn 20.0](https://gunicorn.org/) - Python WSGI HTTP Server for UNIX

## Authors

* **[Denis Sharhov](https://github.com/Denisscore)**
* **[Andrew Smelov](https://github.com/IzmdI)**
* **[Vitaliy Mikhaylov](https://github.com/fsowme)**
