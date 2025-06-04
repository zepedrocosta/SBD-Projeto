#!/usr/bin/tclsh

# Set Database & Benchmark
dbset db maria
dbset bm TPC-C

# DB configs
diset connection maria_host 172.22.0.4
diset connection maria_port 3306
diset connection mysql_socket "/var/run/mysqld/mysqld.sock"
diset tpcc maria_user tpcc
diset tpcc maria_pass tpcc
diset tpcc maria_dbase tpcc

# Default for WH and VU
diset tpcc maria_count_ware 50
diset tpcc maria_num_vu 10

# Driver script options
diset tpcc maria_timeprofile true
diset tpcc maria_async_scale false
diset tpcc maria_driver timed

# Ensure test is limited by time
diset tpcc maria_total_iterations 1000000

# Timed duration
diset tpcc maria_rampup 2
diset tpcc maria_duration 8

# Distribute load
diset tpcc maria_allwarehouse false

# Transactions options
tcset refreshrate 10
tcset logtotemp 1
tcset unique 1
tcset timestamps 1

# Run

foreach z {2 4 8 12} {
    set w [expr {$z * 5}]
    puts "Building Schema for $z TEST"

    # Delete possible previous data
    deleteschema
    vudestroy

    # Build and load
    buildschema
    vudestroy
    loadscript

    # Vuser options
    vuset delay 500
    vuset repeat 500
    vuset iterations 1
    vuset showoutput 0
    vuset logtotemp 1
    vuset unique 1
    vuset nobuff 0
    vuset timestamps 1

    puts "Starting $z VU TEST"
    tcstart
    vuset vu $z
    vucreate
    vurun

    puts "Waiting 1 for cleanup and collection"
    after 60000

    puts "Destroying VU"
    vudestroy
    tcstop
}