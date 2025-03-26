FROM python:3.10-slim AS builder
WORKDIR /servers_configurator
COPY ./servers_configurator/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
COPY ./servers_configurator .

FROM python:3.10-slim
WORKDIR /servers_configurator
COPY --from=builder /root/.local /root/.local
COPY ./servers_configurator .
ENV PATH=/root/.local/bin:$PATH

WORKDIR /
ENTRYPOINT [ "python3", "-m", "servers_configurator"]
