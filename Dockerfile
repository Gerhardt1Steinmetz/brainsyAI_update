FROM python:3.10

WORKDIR /code/app

COPY ./requirements.txt /code/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

COPY . /code/app

# Heroku injects a $PORT env var that they control - not my favorite that we can't specify, but oh well.
CMD uvicorn main:app --host 0.0.0.0 --port "$PORT"