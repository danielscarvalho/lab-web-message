#!/bin/bash
# Launch Cloud Shell and run the following commands to deploy the application to Google Cloud Run serverless:
gcloud init && \
gcloud config set project lab-web-495417 && \
gcloud run deploy webmessage \
  --source . \
  --region us-east1 \
  --allow-unauthenticated 
#  --set-env-vars PGHOST=...,PGUSER=...,PGDATABASE=... \
#  --set-secrets PGPASSWORD=pgpassword:latest
