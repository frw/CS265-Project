#!/usr/bin/env python

import csv
import os
import sys
import timeit

num = sys.argv[1]
output = open('results_static_workload.csv', 'w')
writer = csv.writer(output, delimiter=',')

read_percentages = []
control_results = []
experimental_results = []
for i in range(11):
    read_percent = i * 10
    read_percentages.append(read_percent)
    
    control = "/Users/emasatsugu/Desktop/CS265/Project/CS265-Project/rocksdb/db_bench --use_existing_db=0 --num=" + str(num) + " --level0_stop_writes_trigger=20 --level0_slowdown_writes_trigger=12 --level0_file_num_compaction_trigger=4 --statistics=0 --benchmarks=readwritegranular --allow_defer_compaction=false --readwritelst=" + str(read_percent) + " > /dev/null"
    experimental = "/Users/emasatsugu/Desktop/CS265/Project/CS265-Project/rocksdb/db_bench --use_existing_db=0 --num=" + str(num) + " --level0_stop_writes_trigger=500 --level0_slowdown_writes_trigger=500 --level0_file_num_compaction_trigger=4 --statistics=0 --benchmarks=readwritegranular --allow_defer_compaction=true --readwritelst=" + str(read_percent) + " > /dev/null"

    control_total_time = 0
    experimental_total_time = 0
    
    for run in range(10):
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

