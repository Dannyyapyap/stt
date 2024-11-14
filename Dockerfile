# Dependencies stage
FROM python:3.12.3 AS compile-image

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \ 
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements and install Python dependencies into virtual env
COPY requirements.txt .
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12.3-slim AS build-image

WORKDIR /app

## Copy virtual env from the first stage
COPY --from=compile-image /venv /venv

## Install runtime deps and FFMPEG
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH="/venv/bin:$PATH" \
    PYTHONPATH=/app \
    DATABASE_PATH=/transcriptions.db

# Copy app code
COPY app/ .

EXPOSE 8020

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8020", "--log-level", "info"]