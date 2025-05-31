#!/usr/bin/tclsh

# Set Database & Benchmark
dbset db pg
dbset bm TPC-C

# DB configs
diset connection pg_host posgres-database
diset connection pg_port 5432
diset connection pg_sslmode false
diset tpcc pg_superuser postgres
diset tpcc pg_superuserpass 1234
diset tpcc pg_defaultdb postgres
diset tpcc pg_user tpcc
diset tpcc pg_pass tpcc
diset tpcc pg_dbase tpcc
diset tpcc pg_tspace pg_default

# Default for WH and VU
diset tpcc pg_count_ware 80
diset tpcc pg_num_vu 4

# Driver script options
diset tpcc pg_timeprofile true
diset tpcc pg_async_scale false
diset tpcc pg_driver timed

# Ensure test is limited by time
diset tpcc pg_total_iterations 1000000

# Timed duration
diset tpcc pg_rampup 2
diset tpcc pg_duration 13

# Distribute load
diset tpcc pg_allwarehouse false

# Transactions options
tcset refreshrate 10
tcset logtotemp 1
tcset unique 1
tcset timestamps 1

# Delete possible previous data
deleteschema
vudestroy

# Build and load
buildschema
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

# Run
tcstart

foreach z {4 8 12 16 32} {
    puts "Starting $z VU TEST"

    puts "Setting $z VU"
    vuset vu $z

    puts "Running $z VU"
    vucreate
    vurun

    puts "Waiting 1 for cleanup and collection"
    after 60000

    puts "Destroying VU"
    vudestroy
}

tcstop
