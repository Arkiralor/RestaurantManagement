# Repository Boilerplate

A boilerplate that can be used as a template for quickly setting up a repository for a web application with the following stacks:

1. __Backend__ in [_Django_](https://www.djangoproject.com/) & [_Django Restframework_](https://www.django-rest-framework.org/)
2. __Frontend__ in [_ReactJS_](https://react.dev/)
3. __Application__ in [_React Native_](https://reactnative.dev/)
4. __Stable Storage__ in [_PostgreSQL_](https://www.postgresql.org/)
5. __Warehousing/Lake__ in [_MongoDB_](https://www.mongodb.com/)
6. __In-Memory Datasource__ in [_Redis_](https://redis.io/)

## Setup

The setup procedures are defined as follows

### Pre-Requisites

1. __Console__: _[BASH](https://www.gnu.org/software/bash/)_
    - _[GitBASH](https://git-scm.com/downloads)_ for __Windows__
2. __[Python](https://www.python.org/)__ _v3.9_
3. __[PostreSQL](https://www.postgresql.org/)__ & __[PGAdmin](https://www.pgadmin.org/)__
4. __[MongoDB](https://www.mongodb.com/)__ & __[MongoDB Compass](https://www.mongodb.com/products/compass)__
5. __[Redis](https://redis.io/)__
6. __[Crontab](https://man7.org/linux/man-pages/man5/crontab.5.html)__

#### Backend Setup

__IMPORTANT:__ `Redis` and `cron` are not available for windows-systems; if you have no choice but to use a windows machine, we suggest using a [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) instance to setup the repository, although it is not an ideal solution as sometimes, the code breaks on WSL.

#### Respository Setup

1. `python -m venv env`
2. `source env/bin/activate`
    - `source env/Scripts/activate` in Windows.
3. `python -m pip install pip-tools`
4. `sh scripts/install_dependencies.sh`
5. Copy the `.env` file for the backend into the folder and fill the values as per your local configuration.
6. `crontab -e` to open the `cron` config file.
   1. `* * * * * path/to/python/executable path/to/manage.py runcrons --silent` to enable the cron jobs defined in the system.
   2. `^o` to write the changes to the file buffer (press `Enter` when prompted)
   3. `^x` to exit the file editor.
7. `python manage.py makemigrations`
8. `python manage.py migrate`
9. `python manage.py createsuperuser`

    __FOR LOCAL DEV MACHINE ONLY__

    ```sh
    USERNAME: admin
    EMAIL: admin@admin.com
    PASSWORD: password
    ```

10. `sh scripts/run_server.sh`

#### .ENV File Format

```env
## General Settings:
APP_NAME = "The name of your application"
DOMAIN_URL = "The domain of your application"
OWNER_EMAIL = "Your official email address"
CONTACT_EMAIL = "Contact email for your application"


## System Settings:
SECRET_KEY = "Secret key for site encryption (one-way)"
DEBUG = True | False
ENV_TYPE = "DEV" | "PROD" | "TEST" | "QA"
ALLOWED_HOSTS = "host 1, host 2, host 3, host 4, ..."
JWT_ALGORITHM = "HS256"
CORS_ORIGIN_WHITELIST = "origin 1, origin 2, origin 3, origin 4, ..."

## Database Settings:
DB_NAME = "Name of SQL database"
DB_HOST = "Host for SQL database"
DB_PORT = "Posrt for SQL database"
DB_USER = "Username for SQL database"
DB_PASSWORD = "Password for SQL database"

## MongoDB Settings:
MONGO_URI = "URI for MongoDB"
MONGO_NAME = "Name of MongoDB cluster"
MONGO_HOST = "Host for MongoDB cluster"
MONGO_PORT = "Port for MongoDB cluster"
MONGO_USER = "Username for MongoDB cluster"
MONGO_PASSWORD = "Password for MongoDB cluster"

## Internationalization Settings:
LANGUAGE_CODE = " "
TIME_ZONE = " "
USE_I18N = True | False
USE_TZ = True | False

## Authentication Settings:
OTP_ATTEMPT_LIMIT = How many login attempts before being blocked
OTP_ATTEMPT_TIMEOUT = How long to block for

## Amazon Web Services Settings:
SNS_SENDER_ID = ""
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_REGION_NAME = ""
```

#### Documentation

1. [Postman](https://documenter.getpostman.com/view/17779018/2s93Y3wh65)
2. [JSON](https://github.com/Arkiralor/ProjectBoilerplate/blob/master/docs/backend/backend_postman_collection.json)

#### PostgreSQL/PGADmin Setup

Details [here](https://www.postgresql.org/docs/current/tutorial-install.html).

#### MongoDB/Compass Setup

Details [here](https://www.mongodb.com/docs/manual/administration/install-community/).

#### Redis Setup

Details [here](https://redis.io/docs/getting-started/installation/).
