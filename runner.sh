#!/bin/bash

# Set your container names
HAMMER_CONTAINER=HammerDB_SBD
DB_CONTAINER=db_container

SYS_STATS_LOG=sys_stats.log

# TCL script path (on host or mounted in container)
TCL_SCRIPT=/home/HammerDB-4.10/scripts/tcl-scripts/largeTestMySQL.tcl

> $SYS_STATS_LOG

(while true; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')% RAM: $(free -m | awk '/Mem:/ { printf("%.2f"), $3/$2 * 100.0 }')%" >> $SYS_STATS_LOG
    sleep 10
done) &
SYS_STATS_PID=$!

# Ensure system stats logging stops when script exits
trap "kill $SYS_STATS_PID" EXIT

# Run the HammerDB benchmark from the HammerDB container
docker exec -i $HAMMER_CONTAINER /home/HammerDB-4.10/hammerdbcli auto $TCL_SCRIPT
