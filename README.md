# LegalBot Backend

## Before starting

See `Deployment` and `Pre-requisites` to know how to install and deploy the project

## Pre-requisites

- Docker
- Docker-compose

## Make commands
Use this command `export COMPOSE_FILE=local.yml` after to use commands make
```
make up
-- Start the containers
```

```
make stop
-- Stop docker containers whitout removing them
```

```
make down
-- Stop and remove docker containers
```

```
make build
-- Rebuild docker image
```
## Dev commands
This commands only work's inside backend container, for use it, you must use `make up` first
```
dev up
-- Run the application
```

```
dev pipi
-- Install requirements
```

```
dev makemig
-- Make migrations
```

```
dev migrate
-- Migrate pending migrations
```


```
dev createapp <APP_NAME>
-- Create Django App
```

## Or change previous commands docker for docker-compose ...

This command `export COMPOSE_FILE=local.yml` is used to enable the use of docker-compose up, etc. without using -f local.yml ..

```
docker-compose up
-- Run the application
```

```
docker-compose build
-- Rebuild docker image
```

```
docker-compose down
-- Stop and remove docker containers
```

## Enable debugger and remove django container

A good practice is to separate django from postgres, redis and celery, because this will allow us to run django separately so that it allows us to iterate with it. The others will continue running normally, but separate from django.

```
docker-compose up
-- Run the application
```

```
docker-compose ps
-- See the containers that run
```

```
docker rm -f bajonazo-backend_django_1
-- Remove Django service
```

```
docker-compose run --rm --service-ports django
-- detach Django services
```

## Delete the volume from the database

It is advisable to always do this process when we are in prod, because it is cleaner to delete the migrations. But if we are in production it is advisable to use squash migrations.

```
docker-compose ps
-- See the containers that run
```

```
docker-compose down
-- Stop and remove docker containers
```

```
docker volume ls
-- See volumes docker
```

```
docker volume rm -f bajonazo-backend_local_postgres_data
-- clear volume
```

```
docker-compose run --rm django python manage.py makemigrations
-- Apply makemigrations
```

```
docker-compose run --rm django python manage.py migrate
-- Migrate pending migrations
```

Finally

```
docker-compose up
-- Run the application
```

# IMPORTANT
## Development process on local
1. Start the containers with `make up`
2. Inside the backend container install the depencencies with `dev pipi`
3. Run the application with `dev up`
4. Code
