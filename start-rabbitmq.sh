#!/usr/bin/env bash

set -euo pipefail

STATE="$(podman ps -a --format "{{.State}}" --filter name=rabbitmq_dev)"
if [[ "${STATE}" == "running" ]] ; then
    echo "RabbitMQ container already running"
    exit 0
fi

if [[ "${STATE}" == "exited" ]] ; then
    podman start rabbitmq_dev
    exit 0
fi

podman run -d --hostname rabbitmq_dev --name rabbitmq_dev -p 5672:5672 -p 15672:15672 -v rabbitmq_data:/var/lib/rabbitmq/ docker.io/rabbitmq:3.12-management
