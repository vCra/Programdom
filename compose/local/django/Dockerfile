FROM node:alpine as static
COPY package.json /package.json
RUN npm install -g gulp
RUN npm install
WORKDIR /static
COPY ./programdom/static /programdom/static
COPY ./gulpfile.prod.js /gulpfile.js
RUN gulp build


FROM python:3.7-alpine
COPY --from=static /static /app/programdom/static
ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Translations dependencies
  && apk add gettext \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apk add postgresql-client \
  && apk add libxml2-dev libxslt-dev


# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/production.txt

COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY . /app

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
