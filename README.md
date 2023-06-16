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

## ¿How to enter bash from windows?
```
- Step 1: open your powershell
- Step 2: `docker exec -it legalbot_backend bash`
          *Run this command to enter the bash(docker container) of legalbot_backend   
```

## What commands can I use if I am in bash from windows?
`you can use these commands (example):`
```
python3 manage.py migrate
-- Migrate pending migrations
```

```
coverage run --source='legalbot/apps/users' -m pytest legalbot/apps/users/tests/test_providers/tests_admin.py
-- Command to see the coverage of the tests
```

```
pip3 install -r requirements.txt
-- Install requirements
```


## How to run Tests?

To run the tests you must do this command(example):
`dev test legalbot/apps/users/tests/test_providers/tests_admin.py -v`

How to run the tests created in a file?

```
dev test <file directory> -v
-- Run the tests created by applications
```

¿How do test commands work?

```
dev test
-- Check all the project files and if there is a code mess it will indicate that you should run Black or Isort
```

```
dev black
-- Order lines of code
```

```
dev isort
-- Order lines of code
```

# IMPORTANT
## Development process on local
1. Start the containers with `make up`
2. Inside the backend container install the depencencies with `dev pipi`
3. Run the application with `dev up`
4. Code
