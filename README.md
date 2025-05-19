# Коворкинг

## Веб-приложение для текстового и голосового общения в сети

Проект находится в разработке

### Инструкция по запуску

1. Создать и заполнить конфигурационный файл:
```
cp .env.example .env
```
Изменить там переменные среды

2. Настроить конфиг source/web/typescript/web/.env

```
cp .env.docker .env
```

3. Настроить конфиг /source/nginx\_gateway/nginx.conf

- в /source/nginx\_gateway/ssl следовать инструкциям README файла
- в nginx.conf исправить директиву server\_name в локации server на необходимый домен

4. Запустить проект

```
docker compose up
``` 
