#!/bin/bash

# Set your container names
HAMMER_CONTAINER=HammerDB_SBD

echo "Starting HammerDB benchmark runner..."

##################################################################
# Setup containers
##################################################################

# Compose down to ensure a clean start

# TCL script path (on host or mounted in container)
echo "Stopping and removing existing containers, images and volumes..."

docker compose down --rmi all -v

sleep 5

# Compose up to start the containers
echo "Starting containers..."

docker compose up -d

sleep 10

echo "Containers are up and running!"

echo "Starting HammerDB benchmark..."

##################################################################
# POSTGRESQL
##################################################################

echo "Starting up PostgreSQL benchmark..."

# Start the stats logging in the background
./PCStats.sh "postgres" &
PCSTATS_PID=$!

# Wait 5 seconds for stats logger to initialize
sleep 5

# Run the benchmark via Docker
docker exec -i "$HAMMER_CONTAINER" /home/HammerDB-4.10/hammerdbcli auto scripts/tcl-scripts/largeTestPG.tcl

# Kill the PCStats logger
kill "$PCSTATS_PID"

echo "Benchmark and monitoring complete for PostgreSQL."

# Wait 30 seconds before exiting
sleep 30

##################################################################
# MYSQL
##################################################################

echo "Starting up MySQL benchmark..."

# Start the stats logging in the background
./PCStats.sh "mysql" &
PCSTATS_PID=$!

# Wait 5 seconds for stats logger to initialize
sleep 5

# Run the benchmark via Docker
docker exec -i "$HAMMER_CONTAINER" /home/HammerDB-4.10/hammerdbcli auto scripts/tcl-scripts/largeTestMySQL.tcl

# Kill the PCStats logger
kill "$PCSTATS_PID"

echo "Benchmark and monitoring complete for MySQL."

# Wait 30 seconds before exiting
sleep 30

##################################################################
# MARIADB
##################################################################

echo "Starting up MariaDB benchmark..."

# Start the stats logging in the background
./PCStats.sh "mariadb" &
PCSTATS_PID=$!

# Wait 5 seconds for stats logger to initialize
sleep 5

# Run the benchmark via Docker
docker exec -i "$HAMMER_CONTAINER" /home/HammerDB-4.10/hammerdbcli auto scripts/tcl-scripts/largeTestMariaDB.tcl

# Kill the PCStats logger
kill "$PCSTATS_PID"

echo "Benchmark and monitoring complete for MariaDB."

echo "Benchmark and monitoring complete."
