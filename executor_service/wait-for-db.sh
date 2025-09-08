#!/bin/sh
# wait-for-db.sh

set -e

host="$1"
shift
cmd="$@"

until nc -z "$host" 5432; do
  >&2 echo "Postgres no está disponible todavía - durmiendo"
  sleep 1
done

>&2 echo "Postgres está disponible - ejecutando comando"
exec $cmd