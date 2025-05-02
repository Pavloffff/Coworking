FROM node:20 as builder
WORKDIR /app

RUN apt update -y
RUN apt install python3 -y
RUN apt install python3-pip -y

COPY ./rtc_producer/package.json ./rtc_producer/package-lock.json ./

RUN npm ci --production

COPY ./rtc_producer/ ./

EXPOSE 3031
EXPOSE 40000-41000/udp
ENV NODE_ENV=production

CMD ["node", "server.js"]
