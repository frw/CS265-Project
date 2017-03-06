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

# Returns the read and write costs of the read-optimized version of the LSM tree
def read_optimized():
    read_cost = L * ( np.log(F) + np.log(P) )
    write_cost = L * 2 * ( P + F * P )
    
    return read_cost, write_cost
    
# Returns the read and write costs of the write-optimized version of the LSM tree
def write_optimized():
    read_cost = L * ( np.log(F) + np.log(P) + B )
    write_cost = L * 2 * B
    
    return read_cost, write_cost
    
# Returns the read and write costs of the intermediate version of the LSM tree
def intermediate():
    read_cost = L * ( np.log(F) + np.log(P) + np.log(B) )
    write_cost = L * ( B + B * np.log(B) )
    
    return read_cost, write_cost

costs = [read_optimized(), write_optimized(), intermediate()]
legends = ['Read Optimized', 'Write Optimized', 'Intermediate']
colors = ['r', 'g', 'b']
    
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
