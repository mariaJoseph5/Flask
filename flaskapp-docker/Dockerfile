# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster
FROM ubuntu:18.04

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y
# Install pip requirements
COPY requirements.txt .
COPY flaskapp /opt/
RUN pip3 install -r requirements.txt

WORKDIR /opt/
COPY . /opt/

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn3", "--bind", "0.0.0.0:8000", "app:app", "--workers=5"]
