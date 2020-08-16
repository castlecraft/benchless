#!/bin/bash
cat <<EOF > sites/common_site_config.json
{
 "db_host": "0.0.0.0",
 "db_port": 3306,
 "redis_cache": "redis://localhost:13000",
 "redis_queue": "redis://localhost:11000",
 "redis_socketio": "redis://localhost:12000"
}
EOF
