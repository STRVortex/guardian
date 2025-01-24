FROM python:3.9-slim
WORKDIR /app
COPY . /app/
RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    RUN pip install --no-cache-dir --upgrade -r requirements.txt
    RUN chmod +x start.sh
    CMD ["bash", "start.sh"]