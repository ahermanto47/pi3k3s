#!/bin/bash

for SERVICE_ID in $(docker service ls -q); do
  SERVICE_NAME=$(docker service inspect --format '{{.Spec.Name}}' $SERVICE_ID)

  # Check if all tasks are in a 'shutdown' or 'complete' state for this service
  # We look for any tasks that are *not* in these states.
  RUNNING_TASKS=$(docker service ps $SERVICE_ID --filter "desired-state=running" -q)

  if [ -z "$RUNNING_TASKS" ]; then
    # No running tasks, means it's likely a completed or failed one-shot service
    echo "Service '$SERVICE_NAME' (ID: $SERVICE_ID) has no running tasks. Removing..."
    docker service rm $SERVICE_ID
  else
    echo "Service '$SERVICE_NAME' (ID: $SERVICE_ID) has running tasks. Skipping removal."
  fi
done
