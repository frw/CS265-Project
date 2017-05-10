#!/usr/bin/env python

import csv
import os
import sys
import timeit

from config import *

output = open('results_skewed_workload.csv', 'w')
writer = csv.writer(output, delimiter=',')

read_percentages = []
control_results = []
experimental_results = []
for read_percent in range(11):
    read_percent *= 10
    read_percentages.append(read_percent)

    readwritelst = str(read_percent) + "," + str(100 - read_percent)
    control = DB_BENCH_CMD + " --use_existing_db=0 --num=" + str(NUM) + " --level0_stop_writes_trigger=20 --level0_slowdown_writes_trigger=12 --level0_file_num_compaction_trigger=4 --statistics=0 --benchmarks=readwritegranular --allow_defer_compaction=false --readwritelst=" + readwritelst + " > /dev/null"
    experimental = DB_BENCH_CMD + " --use_existing_db=0 --num=" + str(NUM) + " --level0_stop_writes_trigger=500 --level0_slowdown_writes_trigger=500 --level0_file_num_compaction_trigger=4 --statistics=0 --benchmarks=readwritegranular --allow_defer_compaction=true --readwritelst=" + readwritelst + " > /dev/null"

    control_total_time = 0
    experimental_total_time = 0

    for run in range(TRIALS):
        # Run control
        start_time = timeit.default_timer()
        os.system(control)
        end_time = timeit.default_timer()
        control_total_time += (end_time - start_time)

        # Run experimental
        start_time = timeit.default_timer()
        os.system(experimental)
        end_time = timeit.default_timer()
        experimental_total_time += (end_time - start_time)

    control_results.append(control_total_time / 10)
    experimental_results.append(experimental_total_time / 10)

columns = [read_percentages, control_results, experimental_results]
rows = zip(*columns)
writer.writerow(["Read percentages", "Control", "Experimental"])
for row in rows:
    writer.writerow(row)

output.close()

