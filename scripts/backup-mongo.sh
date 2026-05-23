#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -f "$ROOT_DIR/.env" ]; then
  set -a
  . "$ROOT_DIR/.env"
  set +a
fi

BACKUP_DIR="${BACKUP_DIR:-/backups}"
MONGO_CONTAINER_NAME="${MONGO_CONTAINER_NAME:-qa_mongo}"
MONGO_DB_NAME="${MONGO_DB_NAME:-qa_platform}"
MONGO_USERNAME="${MONGO_USERNAME:-${MONGO_INITDB_ROOT_USERNAME:-admin}}"
MONGO_PASSWORD="${MONGO_PASSWORD:-${MONGO_INITDB_ROOT_PASSWORD:-change-me}}"
MONGO_AUTH_SOURCE="${MONGO_AUTH_SOURCE:-$MONGO_DB_NAME}"
TIMESTAMP="$(date +'%Y-%m-%d-%H-%M')"
TEMP_DIR="$(mktemp -d)"
ARCHIVE_FILE="$BACKUP_DIR/$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"

docker exec \
  -e MONGO_USERNAME="$MONGO_USERNAME" \
  -e MONGO_PASSWORD="$MONGO_PASSWORD" \
  -e MONGO_AUTH_SOURCE="$MONGO_AUTH_SOURCE" \
  "$MONGO_CONTAINER_NAME" \
  sh -lc "rm -rf /tmp/mongo-backup && mkdir -p /tmp/mongo-backup && mongodump --db '$MONGO_DB_NAME' --out /tmp/mongo-backup --username '$MONGO_USERNAME' --password '$MONGO_PASSWORD' --authenticationDatabase '$MONGO_AUTH_SOURCE'"

docker cp "$MONGO_CONTAINER_NAME:/tmp/mongo-backup/." "$TEMP_DIR/"
tar -czf "$ARCHIVE_FILE" -C "$TEMP_DIR" .
rm -rf "$TEMP_DIR"

docker exec "$MONGO_CONTAINER_NAME" sh -lc "rm -rf /tmp/mongo-backup"

find "$BACKUP_DIR" -type f -name '*.tar.gz' -mtime +7 -delete

echo "Backup written to $ARCHIVE_FILE"
