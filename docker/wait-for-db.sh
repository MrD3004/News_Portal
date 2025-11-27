#!/usr/bin/env bash
set -e

echo "Waiting for MySQL at ${DB_HOST}:${DB_PORT}..."
until nc -z "${DB_HOST}" "${DB_PORT}"; do
  sleep 2
done
echo "MySQL is up."





