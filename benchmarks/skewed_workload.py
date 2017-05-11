#!/usr/bin/env python

import csv
import os
import sys
import timeit
import shutil

from config import *

output = open('results_skewed_workload.csv', 'w')
writer = csv.writer(output, delimiter=',')

read_percentages = []
control_results = []
control_read_results = []
control_write_results = []
experimental_results = []
experimental_read_results = []
experimental_write_results = []
for read_percent in range(11):
    read_percent *= 10
    read_percentages.append(read_percent)

    readwritelst = str(read_percent) + "," + str(100 - read_percent)
    control = DB_BENCH_CMD + " --use_existing_db=1 --num=" + str(NUM) + " --level0_stop_writes_trigger=20 --level0_slowdown_writes_trigger=12 --level0_file_num_compaction_trigger=4 --statistics=0 --benchmarks=readwritegranular --allow_defer_compaction=false --readwritelst=" + readwritelst + " > /dev/null"
    experimental = DB_BENCH_CMD + " --use_existing_db=1 --num=" + str(NUM) + " --level0_stop_writes_trigger=500 --level0_slowdown_writes_trigger=500 --level0_file_num_compaction_trigger=4 --statistics=0 --benchmarks=readwritegranular --allow_defer_compaction=true --readwritelst=" + readwritelst + " > /dev/null"

    control_total_time = 0
    control_total_read_throughput = 0
    control_total_write_throughput = 0
    experimental_total_time = 0
    experimental_total_read_throughput = 0
    experimental_total_write_throughput = 0

    for run in range(TRIALS):
        print "Skewed Workload (Read percent: %s, Trial no.: %s)" % (read_percent, run)

        shutil.rmtree(DB_LOCATION)
        shutil.copytree(DB_EXISTING, DB_LOCATION)

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
        os.remove('example.txt')

        shutil.rmtree(DB_LOCATION)
        shutil.copytree(DB_EXISTING, DB_LOCATION)

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
        os.remove('example.txt')

    control_results.append(control_total_time / TRIALS)
    control_read_results.append(control_total_read_throughput / TRIALS)
    control_write_results.append(control_total_write_throughput / TRIALS)
    experimental_results.append(experimental_total_time / TRIALS)
    experimental_read_results.append(experimental_total_read_throughput / TRIALS)
    experimental_write_results.append(experimental_total_write_throughput / TRIALS)

    print control_results[-1], control_read_results[-1], control_write_results[-1], \
          experimental_results[-1], experimental_read_results[-1], experimental_write_results[-1]

columns = [read_percentages, control_results, control_read_results, control_write_results, experimental_results, experimental_read_results, experimental_write_results]
rows = zip(*columns)
writer.writerow(["Read percentages", "Control", "ControlReads", "ControlWrites", "Experimental", "ExperimentalReads", "ExperimentalWrites"])
for row in rows:
    writer.writerow(row)

output.close()

