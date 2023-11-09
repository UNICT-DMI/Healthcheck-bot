#!/bin/bash

config_file="config/settings.yaml"
stop_flag="stop.flag"

cleanup() {
    echo " Stopping..."
    rm -f "$stop_flag"
    exit 0
}

if [ ! -f "$config_file" ]; then
    echo "$config_file not found"
    exit 1
fi

run_timeout=$(sed -n '/run_timeout/s/.*: //p' "$config_file")

trap 'cleanup' INT TERM

while true
do
    if [ -f "$stop_flag" ]; then
        cleanup
    fi

    if ! python3 src/main.py; then
        echo "Error in src/main.py..."
    fi

    sleep "$run_timeout"
done
