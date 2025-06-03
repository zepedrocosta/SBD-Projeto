#!/usr/bin/tclsh

# Set Database & Benchmark
dbset db mysql
dbset bm TPC-C

# DB configs
diset connection mysql_host 172.20.0.3
diset connection mysql_port 3307
diset connection mysql_socket "/tmp/mysql.sock"
diset tpcc mysql_user tpcc
diset tpcc mysql_pass tpcc
diset tpcc mysql_dbase tpcc

# Default for WH and VU
diset tpcc mysql_count_ware 80
diset tpcc mysql_num_vu 4

# Driver script options
diset tpcc mysql_timeprofile true
diset tpcc mysql_async_scale false
diset tpcc mysql_driver timed

# Ensure test is limited by time
diset tpcc mysql_total_iterations 1000000

# Timed duration
diset tpcc mysql_rampup 2
diset tpcc mysql_duration 13

# Distribute load
diset tpcc mysql_allwarehouse false

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