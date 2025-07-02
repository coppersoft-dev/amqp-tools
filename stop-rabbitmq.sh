#!/usr/bin/env bash

set -euo pipefail

STATE="$(podman ps -a --format "{{.State}}" --filter name=rabbitmq_dev)"
if [[ "${STATE}" == "exited" ]] ; then
    echo "RabbitMQ container already stopped"
    exit 0
fi

if [[ "${STATE}" == "running" ]] ; then
    podman stop rabbitmq_dev
    exit 0
fi

echo "RabbitMQ container has unknown state '${STATE}'."
echo
echo "Run 'podman ps -a --format json --filter name=rabbitmq_dev' to inspect the container's status and how to stop it manually."
exit 1
