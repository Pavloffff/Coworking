FROM python:3.10-slim AS builder
WORKDIR /notifications_pusher
COPY ./notifications_pusher/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
COPY ./notifications_pusher .

FROM python:3.10-slim
WORKDIR /notifications_pusher
COPY --from=builder /root/.local /root/.local
COPY ./notifications_pusher .
ENV PATH=/root/.local/bin:$PATH
WORKDIR /
ENTRYPOINT [ "python3", "-m", "notifications_pusher"]
