#!/bin/sh

cat <<EOF > Procfile
redis_cache: redis-server --port 13000
redis_socketio: redis-server --port 12000
redis_queue: redis-server --port 11000

socketio: node apps/frappe/socketio.js

web: ./bench_helper serve --port 8000

watch: ./bench_helper watch

schedule: ./bench_helper schedule
worker_short: ./bench_helper worker --queue short
worker_long: ./bench_helper worker --queue long
worker_default: ./bench_helper worker --queue default
EOF
