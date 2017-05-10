#!/usr/bin/env python

import csv
import os
import sys
import timeit

from config import *

output = open('results_static_workload.csv', 'w')
writer = csv.writer(output, delimiter=',')

read_percentages = []
control_results = []
control_read_results = []
control_write_results = []
experimental_results = []
experimental_read_results = []
experimental_write_results = []
for i in range(11):
    read_percent = i * 10
    read_percentages.append(read_percent)

    control = DB_BENCH_CMD + " --use_existing_db=0 --num=" + str(NUM) + " --level0_stop_writes_trigger=20 --level0_slowdown_writes_trigger=12 --level0_file_num_compaction_trigger=4 --statistics=0 --benchmarks=readwritegranular --allow_defer_compaction=false --readwritelst=" + str(read_percent) + " > /dev/null"
    experimental = DB_BENCH_CMD + " --use_existing_db=0 --num=" + str(NUM) + " --level0_stop_writes_trigger=500 --level0_slowdown_writes_trigger=500 --level0_file_num_compaction_trigger=4 --statistics=0 --benchmarks=readwritegranular --allow_defer_compaction=true --readwritelst=" + str(read_percent) + " > /dev/null"

    control_total_time = 0
    control_total_read_throughput = 0
    control_total_write_throughput = 0
    experimental_total_time = 0
    experimental_total_read_throughput = 0
    experimental_total_write_throughput = 0

    for run in range(TRIALS):
        print "Static Workload (Read percent: %s, Trial no.: %s)" % (read_percent, run)

        # Run control
        start_time = timeit.default_timer()
        os.system(control)
        end_time = timeit.default_timer()
        control_total_time += (end_time - start_time)

        # Read file to get control read+write throughput
        f = open('example.txt', 'r')
        control_total_read_throughput += float(f.readline().strip())
        control_total_write_throughput += float(f.readline().strip())
        f.close()

        # Run experimental
        start_time = timeit.default_timer()
        os.system(experimental)
        end_time = timeit.default_timer()
        experimental_total_time += (end_time - start_time)

        # Read file to get experimental read+write throughput
        f = open('example.txt', 'r')
        experimental_total_read_throughput += float(f.readline().strip())
        experimental_total_write_throughput += float(f.readline().strip())
        f.close()

    control_results.append(control_total_time / TRIALS)
    control_read_results.append(control_total_read_throughput / TRIALS)
    control_write_results.append(control_total_write_throughput / TRIALS)
    experimental_results.append(experimental_total_time / TRIALS)
    experimental_read_results.append(experimental_total_read_throughput / TRIALS)
    experimental_write_results.append(experimental_total_write_throughput / TRIALS)

columns = [read_percentages, control_results, control_read_results, control_write_results, experimental_results, experimental_read_results, experimental_write_results]
rows = zip(*columns)
writer.writerow(["Read percentages", "Control", "ControlReads", "ControlWrites", "Experimental", "ExperimentalReads", "ExperimentalWrites"])
for row in rows:
    writer.writerow(row)

output.close()

