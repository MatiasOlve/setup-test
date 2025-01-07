# Backend Dockerfile
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the backend folder and requirements
COPY backend/ /app/backend/
COPY requirements.txt /app/
COPY manage.py /app/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    awscli && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add AWS config
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG FORMAT_OUTPUT

RUN aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID && \
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY && \
    aws configure set default.region $AWS_DEFAULT_REGION && \
    aws configure set default.output $FORMAT_OUTPUT

RUN aws codeartifact login \
    --tool pip \
    --repository tinkun \
    --domain tinkun \
    --domain-owner 552699747136 \
    --region us-east-2 && \
    pip config set global.extra-index-url https://pypi.org/simple && \
    pip config set global.trusted-host pypi.org && \
    pip install --no-cache-dir -r requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=backend.settings
ENV PYTHONUNBUFFERED=1

COPY backend/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]