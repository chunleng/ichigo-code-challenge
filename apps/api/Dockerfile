FROM python:3.9-slim
WORKDIR /app
RUN pip install poetry
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
ADD pyproject.toml poetry.lock poetry.toml /app/
RUN poetry install --no-ansi --no-dev
ADD util.py database.py dbseed.py main.py /app/
ADD routers /app/routers
ADD models /app/models

RUN adduser app -h /app -u 1000 -g 1000 -DH
USER 1000

EXPOSE 8000

CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
