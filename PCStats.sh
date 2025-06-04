#!/bin/bash

DB="$1"
interval=10

# Create log file name based on current date and time
timestamp=$(date "+%m_%d_%H_%M")
logfile="sys_usage_${timestamp}_${DB}.csv"

# Write CSV header
echo "Timestamp,CPU_Usage_Percent,RAM_Used_MB" > "$logfile"

while true; do
    # Get current timestamp
    timestamp=$(date "+%Y-%m-%d_%H:%M:%S")
    echo "Current timestamp: $timestamp"

    # Get CPU usage percentage (average over 1 second)
    cpu=$(top -bn2 | grep "Cpu(s)" | tail -n 1 | awk -F'id,' -v prefix="" '{ split($1, vs, ","); cpu=100 - vs[length(vs)]; printf "%.0f", cpu }')

    # Get RAM usage in MB
    mem_total=$(free -m | awk '/Mem:/ {print $2}')
    mem_used=$(free -m | awk '/Mem:/ {print $3}')

    # Write to CSV
    echo "$timestamp,$cpu,$mem_used" >> "$logfile"

    # Wait for interval
    sleep "$interval"
done
