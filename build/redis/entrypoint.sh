#!/bin/bash

REDIS_START="/usr/bin/redis-server /etc/redis.conf"
su - redis -s /bin/sh -c "${REDIS_START}"
