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


# IMPORTANT
## Development process on local
1. Start the containers with `make up`
2. Inside the backend container install the depencencies with `dev pipi`
3. Run the application with `dev up`
4. Code
