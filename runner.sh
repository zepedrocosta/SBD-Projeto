#!/bin/bash

# Set your container names
HAMMER_CONTAINER=HammerDB_SBD
DB_CONTAINER=db_container

# Output log for Docker stats
STATS_LOG=stats.log

# TCL script path (on host or mounted in container)
TCL_SCRIPT= scripts/tcl-scripts/largeTestMySQL.tcl

# Run the HammerDB benchmark from the HammerDB container
docker exec -it $HAMMER_CONTAINER /home/HammerDB-4.10/hammerdbcli auto $TCL_SCRIPT
