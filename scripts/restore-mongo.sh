#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 BACKUP_FILE"
  exit 1
fi

BACKUP_FILE="$1"
if [ ! -f "$BACKUP_FILE" ]; then
  echo "Backup file not found: $BACKUP_FILE"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -f "$ROOT_DIR/.env" ]; then
  set -a
  . "$ROOT_DIR/.env"
  set +a
fi

MONGO_CONTAINER_NAME="${MONGO_CONTAINER_NAME:-qa_mongo}"
MONGO_DB_NAME="${MONGO_DB_NAME:-qa_platform}"
MONGO_USERNAME="${MONGO_USERNAME:-${MONGO_INITDB_ROOT_USERNAME:-admin}}"
MONGO_PASSWORD="${MONGO_PASSWORD:-${MONGO_INITDB_ROOT_PASSWORD:-change-me}}"
MONGO_AUTH_SOURCE="${MONGO_AUTH_SOURCE:-$MONGO_DB_NAME}"
TEMP_DIR="$(mktemp -d)"

trap 'rm -rf "$TEMP_DIR"' EXIT

tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"
docker cp "$TEMP_DIR/." "$MONGO_CONTAINER_NAME:/tmp/mongo-restore"
docker exec \
  -e MONGO_USERNAME="$MONGO_USERNAME" \
  -e MONGO_PASSWORD="$MONGO_PASSWORD" \
  -e MONGO_AUTH_SOURCE="$MONGO_AUTH_SOURCE" \
  "$MONGO_CONTAINER_NAME" \
  sh -lc "mongorestore --drop --db '$MONGO_DB_NAME' /tmp/mongo-restore"

docker exec "$MONGO_CONTAINER_NAME" sh -lc "rm -rf /tmp/mongo-restore"

echo "Restore completed from $BACKUP_FILE"
