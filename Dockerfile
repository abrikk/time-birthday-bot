FROM python:3.8.6

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic
COPY . /app
CMD ["python", "bot.py"]
