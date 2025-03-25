FROM python:3.11-slim

WORKDIR /app
COPY ./servers_configurator .
RUN pip3 install -U -r requirements.txt

ENTRYPOINT [ "python3", "-m", "."]
