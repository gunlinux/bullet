#!/bin/sh
# Compare server backends under load with wrk, single worker for apples-to-apples.
#
#   uvicorn      (ASGI)  -> GunbulletApp.__call__
#   granian asgi (ASGI)  -> GunbulletApp.__call__   (isolates the server core)
#   granian rsgi (RSGI)  -> GunbulletApp.__rsgi__   (Rust reads body, 1-call response)
#
# Usage: sh bench_servers.sh [path]   (default path: /age/37)

set -e
PATH_UNDER_TEST="${1:-/age/37}"
DUR=10
THREADS=4
CONNS=64

wait_up() {
  for _ in $(seq 1 50); do
    if curl -s -o /dev/null "http://127.0.0.1:$1$PATH_UNDER_TEST"; then return 0; fi
    sleep 0.2
  done
  echo "server on port $1 never came up"; return 1
}

run_case() {
  name="$1"; port="$2"; shift 2
  "$@" >"/tmp/srv_$port.log" 2>&1 &
  srv_pid=$!
  trap 'kill $srv_pid 2>/dev/null' EXIT
  wait_up "$port"
  echo "================================================================"
  echo "  $name   (http://127.0.0.1:$port$PATH_UNDER_TEST)"
  echo "================================================================"
  wrk -t"$THREADS" -c"$CONNS" -d"${DUR}s" "http://127.0.0.1:$port$PATH_UNDER_TEST"
  kill $srv_pid 2>/dev/null || true
  wait $srv_pid 2>/dev/null || true
  trap - EXIT
  echo
}

run_case "uvicorn / ASGI" 8001 \
  uv run uvicorn main:app_asgi --host 127.0.0.1 --port 8001 --no-access-log --log-level warning

run_case "granian / ASGI" 8002 \
  uv run granian --interface asgi main:app_asgi --host 127.0.0.1 --port 8002 --workers 1 --no-ws --log-level warning

run_case "granian / RSGI" 8003 \
  uv run granian --interface rsgi main:app_asgi --host 127.0.0.1 --port 8003 --workers 1 --no-ws --log-level warning
