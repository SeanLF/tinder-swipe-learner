ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION-alpine

RUN apk add build-base
RUN apk add bash
RUN apk add git
RUN apk add libxml2-dev libxslt-dev

# Upgrade RubyGems and install required Bundler version
RUN pip3 install --upgrade pip

# Create a directory for the app code
WORKDIR /app
ADD requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR /app/server
