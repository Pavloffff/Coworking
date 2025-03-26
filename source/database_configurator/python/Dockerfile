FROM python:3.10-slim AS builder
WORKDIR /database_configurator
COPY ./database_configurator/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
COPY ./database_configurator .

FROM python:3.10-slim
WORKDIR /database_configurator
COPY --from=builder /root/.local /root/.local
COPY ./database_configurator .
ENV PATH=/root/.local/bin:$PATH
WORKDIR /
ENTRYPOINT [ "python3", "-m", "database_configurator"]
