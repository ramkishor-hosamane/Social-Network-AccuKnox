FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

RUN ["python", "manage.py", "makemigrations"]

RUN ["python", "manage.py", "migrate"]

RUN ["python", "manage.py", "create_test_users"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
