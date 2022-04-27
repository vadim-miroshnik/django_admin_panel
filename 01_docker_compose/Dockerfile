# pull official base image
FROM python:3.9-alpine

# set work directory
WORKDIR /usr/src/app
RUN mkdir /usr/src/app/staticfiles

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# define the default command to run when starting the container
CMD ["gunicorn", "--bind", ":8000", "movies.wsgi:application"]