# Flask Blog system

___


## Installation
Client is based on `python 3.6`

To install dependencies use `pipenv` tool and run `pipenv install`

Setup  .env file
-

```
SECRET_KEY=Your_Secret_Key
DEBUG=True

MAIL_USERNAME=test@gmail.com
MAIL_DEFAULT_SENDER=test@gmail.com
MAIL_PASSWORD=mail_pass
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587

REDIS_HOST=localhost
REDIS_PORT=6379
```

Email
---

Email broker implemented on Celery. You need Redis server to run Celery

To run broker execute `celery -A worker.celery worker -l info`

---