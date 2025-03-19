#!/bin/bash

if [[ -z ${PG_START_COMMAND} ]]
then
    echo PG_START_COMMAND env variable is empty
    exit 1
fi

echo "PG_START_COMMAND: {$PG_START_COMMAND}"

LOG_LEVEL=$(printenv LOG_LEVEL)
if [[ -n ${LOG_LEVEL} ]]
then
    PG_START_COMMAND=${PG_START_COMMAND}" --log_min_messages=${LOG_LEVEL}"
fi

su - postgres -c "${PG_START_COMMAND}"
