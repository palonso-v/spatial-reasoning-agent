FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libgl1 \
        libegl1 \
        libglib2.0-0 \
        libusb-1.0-0 \
        libidn2-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY shared ./shared
COPY frontend ./frontend
COPY data ./data
COPY evals ./evals
COPY scripts ./scripts
COPY tests ./tests
COPY pytest.ini .
COPY README.md .

EXPOSE 8000

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]