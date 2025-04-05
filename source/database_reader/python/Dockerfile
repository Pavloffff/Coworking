FROM python:3.10-slim AS builder
WORKDIR /database_reader
COPY ./database_reader/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
COPY ./database_reader .

FROM python:3.10-slim
WORKDIR /database_reader
COPY --from=builder /root/.local /root/.local
COPY ./database_reader .
ENV PATH=/root/.local/bin:$PATH

WORKDIR /
ENTRYPOINT [ "python3", "-m", "database_reader"]
