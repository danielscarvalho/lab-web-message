#!/bin/bash
# Launch Cloud Shell and run the following commands to deploy the application to Google App Engine serverless:
gcloud init && \
gcloud config set project lab-web-495417 && \
gcloud app deploy
