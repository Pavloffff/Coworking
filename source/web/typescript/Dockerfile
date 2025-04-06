FROM node:20 AS build
WORKDIR /app
COPY ./web/package.json ./web/yarn.lock ./
RUN yarn --frozen-lockfile

COPY ./web .
RUN yarn build

FROM nginx:1.25-alpine
COPY ./web/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /srv/www/web
CMD ["nginx", "-g", "daemon off;"]
