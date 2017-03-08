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

# Number of pages in an overflow buffer.
B = 15

# Total number of queries (for looking at read/write ratio)
N = 10

# Returns the read and write costs of the read-optimized version of the LSM tree
def read_optimized(r, w):
    read_cost = L * ( np.log(F) + np.log(P) )
    write_cost = L * 2 * ( P + F * P )
    
    return r * read_cost, w * write_cost
    
# Returns the read and write costs of the write-optimized version of the LSM tree
def write_optimized(r, w):
    read_cost = L * ( np.log(F) + np.log(P) + B )
    write_cost = L * 2 * B
    
    return r * read_cost, w * write_cost
    
# Returns the read and write costs of the intermediate version of the LSM tree
def intermediate(r, w):
    read_cost = L * ( np.log(F) + np.log(P) + np.log(B) )
    write_cost = L * ( B + B * np.log(B) )
    
    return r * read_cost, w * write_cost

linestyles = ['r--', 'r-', 'b--', 'b-', 'g--', 'g-']
labels = ['Read Optimized Reads', 'Read Optimized Writes',
        'Write Optimized Reads', 'Write Optimized Writes',
        'Intermediate Reads', 'Intermediate Writes']
x = range(N + 1)
costs = [[] for i in range(6)]

# Read/Write ratios
for i in range(N + 1):
    w = i
    r = N - i

    read_cost, write_cost = write_optimized(r,w)
    costs[0].append(read_cost / N)
    costs[1].append(write_cost / N)

    read_cost, write_cost = read_optimized(r,w)
    costs[2].append(read_cost / N)
    costs[3].append(write_cost / N)
    
    read_cost, write_cost = intermediate(r,w)
    costs[4].append(read_cost / N)
    costs[5].append(write_cost / N)

lines = []
for i, cost in enumerate(costs):
    line = plt.plot(x, cost, linestyles[i], label=labels[i])
    lines.append(line[0])

plt.legend(lines, labels, loc='upper left')
plt.ylabel('# page accesses')
plt.xlabel('# reads out of 10 queries')
plt.show()

# Single read/write
'''
# x locations of the groups
ind = np.arange(2)

# width of bars
width = 0.15

rects = []
for i in range(len(costs)):
    rect = plt.bar(ind + i * width, costs[i], width, color=colors[i])
    rects.append(rect[0])

plt.xlim((-0.5, 2))
plt.xticks(ind + width * (2 * len(costs) - 3) / 2, ('Read Costs', 'Write Costs'))

plt.legend(rects, legends, loc='upper left')

plt.show()
'''
