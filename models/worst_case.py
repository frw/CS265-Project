from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

# Number of levels in the tree.
L = 5

# Ratio of the size of one level to the next level.
# This is also the expected number of files one has to touch during compaction
# assuming uniform distribution of keys.
F = 3

# Number of pages in a file.
P = 10

# Number of chunks in an overflow buffer.
B = 2

# Number of pages in a chunk.
C = 10

# Current number of writes remaining in the overflow buffer for each level
B_curr = [B * C] * L

# Total number of queries (for looking at read/write ratio)
N = 100

def reset_curr():
    global B_curr

    # Current number of writes remaining in the overflow buffer for each level
    B_curr = [B * C] * L


# Returns the read and write costs of the read-optimized version of the LSM tree
def read_optimized(r, w):
    read_cost = L * ( np.log(F) + np.log(P) )
    write_cost = L * 2 * ( P + F * P )
    
    return r * read_cost, w * write_cost


# Recursively write down levels and track write costs
def write_level(level, number, inter):
    global B_curr
    
    write_cost = 0
    
    if level < L - 1and B_curr[level] < number:
        # Write one chunk down to the next level
        write_cost += write_level(level + 1, C, inter)

        B_curr[level] += C
        
        # Write to now roomy overflow buffer
        B_curr[level] -= number
    else:
        # Write to overflow buffer
        B_curr[level] -= number

    if inter:
        # For intermediate solution, we have to keep the buffer sorted,
        # which means we would have to read through the entire buffer
        write_cost += B * C - B_curr[level] + number
    else:
        write_cost += number
    
    return write_cost


# Returns the read and write costs of the write-optimized version of the LSM tree
def write_optimized(r, w, worst_case=True):
    if worst_case:
        read_cost = L * ( np.log(F) + np.log(P) + B * C )
        write_cost = L * 2 * C

        return r * read_cost, w * write_cost
    else:
        write_cost = 0
        for i in range(w):
            write_cost += write_level(0, 1, False)
        
        read_cost = 0
        # Still worst case read, but read only part of the tree that exists
        for level in range(L):
            read_cost += np.log(F) + np.log(P) + (B * C - B_curr[level])
        read_cost *= r
        
        return read_cost, write_cost


# Returns the read and write costs of the intermediate version of the LSM tree
def intermediate(r, w, worst_case=True):
    if worst_case:
        read_cost = L * ( np.log(F) + np.log(P) + np.log(B * C) )
        write_cost = L * 2 * B * C

        return r * read_cost, w * write_cost
    else:
        write_cost = 0
        for i in range(w):
            write_cost += write_level(0, 1, True)
        
        read_cost = 0
        # Still worst case read, but read only part of the tree that exists
        for level in range(L):
            read_cost += np.log(F) + np.log(P)
            
            buffer_size = B * C - B_curr[level]
            if buffer_size > 0:
                read_cost += np.log(buffer_size)
        read_cost *= r

        return read_cost, write_cost


def set_buffer(buf):
    global B
    B = buf

# Vary buffer size
def vary_b(fig_offset):
    linestyles = ['r--', 'b--', 'g--']
    read_labels = ['Write Optimized Reads',
                   'Intermediate Reads',
                   'Read Optimized Reads']
    write_labels = ['Write Optimized Writes',
                    'Intermediate Writes',
                    'Read Optimized Writes']
    x = []
    read_costs = [[] for i in range(3)]
    write_costs = [[] for i in range(3)]

    for i in range(10):
        B = 2 * (i + 1)
        x.append(B)
        
        r = 1000
        w = 1000
        
        set_buffer(B)
        reset_curr()
        
        read_cost, write_cost = write_optimized(r, w, False)
        reset_curr()
        read_costs[0].append(read_cost / r)
        write_costs[0].append(write_cost / w)
        
        read_cost, write_cost = intermediate(r, w, False)
        reset_curr()
        read_costs[1].append(read_cost / r)
        write_costs[1].append(write_cost / w)
        
        read_cost, write_cost = read_optimized(r, w)
        reset_curr()
        read_costs[2].append(read_cost / r)
        write_costs[2].append(write_cost / w)

    plt.figure(fig_offset)
        
    lines = []
    for i, cost in enumerate(read_costs):
        print cost
        line = plt.plot(x, cost, linestyles[i], label=read_labels[i])
        lines.append(line[0])

    plt.legend(lines, read_labels, loc='upper left', prop={'size':10})
    plt.yscale('log')
    plt.ylim((10, 5000))
    plt.ylabel('Avg # page accesses / read')
    plt.xlabel('Buffer size (in pages)')
    
    plt.savefig('vary_b_reads.png')
    
    #####

    plt.figure(fig_offset + 1)
        
    lines = []
    for i, cost in enumerate(write_costs):
        print cost
        line = plt.plot(x, cost, linestyles[i], label=write_labels[i])
        lines.append(line[0])

    plt.legend(lines, write_labels, loc='upper left', prop={'size':10})
    plt.yscale('log')
    plt.ylim((0, 1200))
    plt.ylabel('Avg # page accesses / write')
    plt.xlabel('Buffer size (in pages)')
    
    plt.savefig('vary_b_writes.png')

# Read/Write ratios
def worst_case_model(fig_offset):
    titles = ['Read Optimized', 'Write Optimized', 'Intermediate']
    linestyles = [['r--', 'r-', 'r:'], ['b--', 'b-', 'b:'], ['g--', 'g-', 'g:']]
    labels = ['Reads', 'Writes', 'Total']
    x = range(N + 1)
    costs = [[[] for i in range(3)] for j in range(3)]

    for i in range(N + 1):
        w = i
        r = N - i

        read_cost, write_cost = write_optimized(r, w)
        costs[0][0].append(read_cost)
        costs[0][1].append(write_cost)
        costs[0][2].append(read_cost + write_cost)

        read_cost, write_cost = read_optimized(r, w)
        costs[1][0].append(read_cost)
        costs[1][1].append(write_cost)
        costs[1][2].append(read_cost + write_cost)

        read_cost, write_cost = intermediate(r, w)
        costs[2][0].append(read_cost)
        costs[2][1].append(write_cost)
        costs[2][2].append(read_cost + write_cost)

    plt.figure(fig_offset)
    f, axes = plt.subplots(1, 3, sharey=True, figsize=(30, 10))
    
    for i in range(3):
        ax = axes[i]
    
        lines = []
        for j, cost in enumerate(costs[i]):
            line = ax.plot(x, cost, linestyles[i][j], label=labels[j])
            lines.append(line[0])

        ax.legend(lines, labels, loc='upper left')
        ax.set_title(titles[i])
        ax.set_ylabel('# page accesses')
        ax.set_xlabel('# reads out of 10 queries')
        
    plt.savefig('worst_case_rw.png')

# Single read/write
def single_model(fig_offset):
    costs = [read_optimized(1, 1), write_optimized(1, 1), intermediate(1, 1)]
    legends = ['Read Optimized', 'Write Optimized', 'Intermediate']
    colors = ['r', 'g', 'b']
        
    # x locations of the groups
    ind = np.arange(2)

    # width of bars
    width = 0.15

    plt.figure(fig_offset)
    
    rects = []
    for i in range(len(costs)):
        rect = plt.bar(ind + i * width, costs[i], width, color=colors[i])
        rects.append(rect[0])

    plt.xlim((-0.5, 2))
    plt.xticks(ind + width * (2 * len(costs) - 3) / 2, ('Read Costs', 'Write Costs'))
    plt.legend(rects, legends, loc='upper left')
    
    plt.savefig('worst_case_single.png')

single_model(1)
vary_b(3)
worst_case_model(2)
