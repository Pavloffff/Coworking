#!/usr/bin/env bash

cmdname=$(basename $0)

echoerr() { if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi }

usage()
{
    cat << USAGE >&2
Usage:
    $cmdname [--hosts=host:port | --host=host:port] [-s] [-t timeout] [-- command args]
    --hosts=host1:port1,host2,port2   List of hosts to test
    -h HOST | --host=HOST             Host or IP under test
    -p PORT | --port=PORT             TCP port under test
    --separator=','                   List separator, default ','
    -s | --strict                     Only execute subcommand if the test succeeds
    -q | --quiet                      Don't output any status messages
    -t TIMEOUT | --timeout=TIMEOUT    Timeout in seconds, zero for no timeout
    -- COMMAND ARGS                   Execute command with args after the test finishes
USAGE
    exit 1
}

wait_for()
{
    if [[ $TIMEOUT -gt 0 ]]; then
        echoerr "$cmdname: waiting $TIMEOUT seconds for $HOST:$PORT"
    else
        echoerr "$cmdname: waiting for $HOST:$PORT without a timeout"
    fi
    start_ts=$(date +%s)
    while :
    do
        if [[ $ISBUSY -eq 1 ]]; then
            nc -z $HOST $PORT
            result=$?
        else
            (echo > /dev/tcp/$HOST/$PORT) >/dev/null 2>&1
            result=$?
        fi
        if [[ $result -eq 0 ]]; then
            end_ts=$(date +%s)
            echoerr "$cmdname: $HOST:$PORT is available after $((end_ts - start_ts)) seconds"
            break
        fi
        sleep 1
    done
    return $result
}

wait_for_wrapper()
{
    if [[ $QUIET -eq 1 ]]; then
        timeout $BUSYTIMEFLAG $TIMEOUT $0 --quiet --child --host=$HOST --port=$PORT --timeout=$TIMEOUT &
    else
        timeout $BUSYTIMEFLAG $TIMEOUT $0 --child --host=$HOST --port=$PORT --timeout=$TIMEOUT &
    fi
    PID=$!
    trap "kill -INT -$PID" INT
    wait $PID
    RESULT=$?
    if [[ $RESULT -ne 0 ]]; then
        echoerr "$cmdname: timeout occurred after waiting $TIMEOUT seconds for $HOST:$PORT"
    fi
    return $RESULT
}

do_wait()
{
    if [[ $CHILD -gt 0 ]]; then
        wait_for
        RESULT=$?
        exit $RESULT
    else
        if [[ $TIMEOUT -gt 0 ]]; then
            wait_for_wrapper
            RESULT=$?
        else
            wait_for
            RESULT=$?
        fi
    fi
}

while [[ $# -gt 0 ]]
do
    case "$1" in
        --hosts=*)
        HOSTS="${1#*=}"
        shift 1
        ;; 
        -h)
        HOST="$2"
        if [[ $HOST == "" ]]; then break; fi
        shift 2
        ;;
        --host=*)
        HOST="${1#*=}"
        shift 1
        ;;
        -p)
        PORT="$2"
        if [[ $PORT == "" ]]; then break; fi
        shift 2
        ;;
        --port=*)
        PORT="${1#*=}"
        shift 1
        ;;  
        --child)
        CHILD=1
        shift 1
        ;;
        -q | --quiet)
        QUIET=1
        shift 1
        ;;
        -s | --strict)
        STRICT=1
        shift 1
        ;;
        --separator=*)
        SEPARATOR="${1#*=}"
        shift 1
        ;;
        -t)
        TIMEOUT="$2"
        if [[ $TIMEOUT == "" ]]; then break; fi
        shift 2
        ;;
        --timeout=*)
        TIMEOUT="${1#*=}"
        shift 1
        ;;
        --)
        shift
        CLI=("$@")
        break
        ;;
        --help)
        usage
        ;;
        *)
        echoerr "Unknown argument: $1"
        usage
        ;;
    esac
done

if [[ -z $HOSTS && -z $HOST ]]; then
    echoerr "Error: you need to provide a list of servers to test."
    usage
fi

if [[ -z $SEPARATOR ]]; then
    SEPARATOR=","
fi

TIMEOUT=${TIMEOUT:-15}
STRICT=${STRICT:-0}
CHILD=${CHILD:-0}
QUIET=${QUIET:-0}

TIMEOUT_PATH=$(realpath $(which timeout))
if [[ $TIMEOUT_PATH =~ "busybox" ]]; then
    ISBUSY=1
    BUSYTIMEFLAG="-t"
else
    ISBUSY=0
    BUSYTIMEFLAG=""
fi

if [[ -n $HOSTS ]]; then
    IFS=$SEPARATOR read -ra hosts_array <<< ${HOSTS}
    for host in ${hosts_array[@]};
    do
        hostport=(${host//:/ })
        HOST=${hostport[0]}
        PORT=${hostport[1]}
        do_wait
    done
else
    do_wait
fi

if [[ $CLI != "" ]]; then
    if [[ $RESULT -ne 0 && $STRICT -eq 1 ]]; then
        echoerr "$cmdname: strict mode, refusing to execute subprocess"
        exit $RESULT
    fi
    exec "${CLI[@]}"
else
    exit $RESULT
fi
