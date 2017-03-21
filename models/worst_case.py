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

# Number of pages in each write
P_in_write = 5

# Number of pages in an overflow buffer.
B = 5

# Current number of writes remaining in the overflow buffer for each level
B_curr = [B / P_in_write] * L

# Total number of queries (for looking at read/write ratio)
N = 100

# Compute number of available writes in each level
W_curr = [0] * L
for i in range(L):
    W_curr[i] = (F ** i) * (P / P_in_write)


def reset_curr():
    global B_curr
    global W_curr

    # Current number of writes remaining in the overflow buffer for each level
    B_curr = [B / P_in_write] * L

    # Compute number of available writes in each level
    W_curr = [0] * L
    for i in range(L):
        W_curr[i] = (F ** i) * (P / P_in_write)


# Returns the read and write costs of the read-optimized version of the LSM tree
def read_optimized(r, w):
    read_cost = L * ( np.log(F) + np.log(P) )
    write_cost = L * 2 * ( P + F * P )
    
    return r * read_cost, w * write_cost


# Recursively write down levels and track write costs
def write_level(level, number, inter):
    global W_curr
    global B_curr
    write_cost = 0
    if W_curr[level] - number  <= -1:
        if B_curr[level] - number <= -1:
            # Write the buffer down to the lower level
            if inter:
                write_cost += write_level(level + 1, (B / P_in_write) - B_curr[level], True)
            else:
                write_cost += write_level(level + 1, (B / P_in_write) - B_curr[level], False)

            if inter:
                # TODO: Need to change this
                write_cost += ( B + B * np.log(B) )
            else:
                write_cost += 2 * B

            B_curr[level] += ((B / P_in_write) - B_curr[level])
            # Write to now roomy overflow buffer
            B_curr[level] -= number
        else:
            # Write to overflow buffer
            B_curr[level] -= number
    else:
        # Write to the current level
        W_curr[level] -= number
    return write_cost


# Returns the read and write costs of the write-optimized version of the LSM tree
def write_optimized(r, w, worst_case=True):
    if worst_case:
        read_cost = L * ( np.log(F) + np.log(P) + B )
        write_cost = L * 2 * B

        return r * read_cost, w * write_cost
    else:
        write_cost = 0
        for write_no in range(w):
            write_cost += write_level(0, 1, False)

        # Still worst case read, but read only part of the tree that exists
        read_cost = 0
        for level in range(L):
            if W_curr[level] == (F ** level) * (P / P_in_write):
                break
            else:
                read_cost += ( np.log(F) + np.log(P) + ((B / P_in_write) - B_curr[level]) * P_in_write )

        return read_cost, write_cost


# Returns the read and write costs of the intermediate version of the LSM tree
def intermediate(r, w, worst_case=True):
    if worst_case:
        read_cost = L * ( np.log(F) + np.log(P) + np.log(B) )
        write_cost = 2 * L * B 

        return r * read_cost, w * write_cost
    else:
        write_cost = 0
        for write_no in range(w):
            write_cost += write_level(0, 1, True)

        # Still worst case read, but read only part of the tree that exists
        read_cost = 0
        for level in range(L):
            if W_curr[level] == (F ** level) * (P / P_in_write):
                break
            else:
                # if buffer exists, include binary scan of it in cost
                if ((B / P_in_write) - B_curr[level]) * P_in_write == 0:
                    read_cost += ( np.log(F) + np.log(P) )
                else:
                    read_cost += ( np.log(F) + np.log(P) + np.log(((B / P_in_write) - B_curr[level]) * P_in_write) )

        return read_cost, write_cost


def set_buffer(buf):
    global B
    B = buf

# Testing complex model
def test_complex_model():
    print write_optimized(100, 100, False)
    reset_curr()
    print intermediate(100, 100, False)
    reset_curr()

# Complex model -- READ plots
def complex_reads():
    linestyles = ['r--', 'b--', 'g--', 'y--']
    labels = ['Write Optimized Reads',
            'Intermediate B=20 Reads',
              'Intermediate B=30 Reads',
              'Intermediate B=40 Reads']
    x = range(N + 1)
    costs = [[] for i in range(4)]

    for i in range(5):
        ratio = 0.1 * (i + 1)
        w = int((1 - ratio) * N)
        r = int(ratio * N)

        read_cost, write_cost = write_optimized(r,w,False)
        reset_curr()
        costs[0].append(read_cost / N)
        #costs[1].append(write_cost / N)
        #costs[1].append((read_cost + write_cost)/ N)

        set_buffer(20)
        reset_curr()
        read_cost, write_cost = intermediate(r,w,False)
        reset_curr()
        costs[1].append(read_cost / N)
        #costs[4].append(write_cost / N)
        #costs[3].append((read_cost + write_cost)/ N)

        set_buffer(30)
        reset_curr()
        read_cost, write_cost = intermediate(r,w,False)
        reset_curr()
        costs[2].append(read_cost / N)
        #costs[7].append(write_cost / N)
        #costs[5].append((read_cost + write_cost)/ N)

        set_buffer(40)
        reset_curr()
        read_cost, write_cost = intermediate(r,w,False)
        reset_curr()
        costs[3].append(read_cost / N)
        #costs[10].append(write_cost / N)
        #costs[7].append((read_cost + write_cost)/ N)

    lines = []
    for i, cost in enumerate(costs):
        x = range(len(cost))
        x = [0.1,0.2,0.3,0.4,0.5]
        print cost
        line = plt.plot(x, cost, linestyles[i], label=labels[i])
        lines.append(line[0])

    plt.legend(lines, labels, loc='upper left', prop={'size':10})
    plt.ylabel('# page accesses')
    plt.xlabel('read/write ratio')
    plt.show()

# Complex model -- WRITE plots
def complex_writes():
    linestyles = ['r--', 'b--', 'g--', 'y--']
    labels = ['Write Optimized Writes',
            'Intermediate B=20 Writes',
              'Intermediate B=30 Writes',
              'Intermediate B=40 Writes']
    x = range(N + 1)
    costs = [[] for i in range(4)]

    for i in range(5):
        ratio = 0.1 * (i + 1)
        w = int((1 - ratio) * N)
        r = int(ratio * N)

        read_cost, write_cost = write_optimized(r,w,False)
        reset_curr()
        #costs[0].append(read_cost / N)
        costs[0].append(write_cost / N)
        #costs[1].append((read_cost + write_cost)/ N)

        set_buffer(20)
        reset_curr()
        read_cost, write_cost = intermediate(r,w,False)
        reset_curr()
        #costs[1].append(read_cost / N)
        costs[1].append(write_cost / N)
        #costs[3].append((read_cost + write_cost)/ N)

        set_buffer(30)
        reset_curr()
        read_cost, write_cost = intermediate(r,w,False)
        reset_curr()
        #costs[2].append(read_cost / N)
        costs[2].append(write_cost / N)
        #costs[5].append((read_cost + write_cost)/ N)

        set_buffer(40)
        reset_curr()
        read_cost, write_cost = intermediate(r,w,False)
        reset_curr()
        #costs[3].append(read_cost / N)
        costs[3].append(write_cost / N)
        #costs[7].append((read_cost + write_cost)/ N)

    lines = []
    for i, cost in enumerate(costs):
        x = range(len(cost))
        x = [0.1,0.2,0.3,0.4,0.5]
        print cost
        line = plt.plot(x, cost, linestyles[i], label=labels[i])
        lines.append(line[0])

    plt.legend(lines, labels, loc='upper left', prop={'size':10})
    plt.ylabel('# page accesses')
    plt.xlabel('read/write ratio')
    plt.show()

# Read/Write ratios
def worst_case_model():
    linestyles = [['r--', 'r-', 'r:'], ['b--', 'b-', 'b:'], ['g--', 'g-', 'g:']]
    labels = [['Read Optimized Reads', 'Read Optimized Writes',
        'Read Optimized Total'],
        ['Write Optimized Reads', 'Write Optimized Writes',
            'Write Optimized Total'],
        ['Intermediate Reads', 'Intermediate Writes', 'Intermediate Total']]
    x = range(N + 1)
    costs = [[[] for i in range(3)] for j in range(3)]

    for i in range(N + 1):
        w = i
        r = N - i

        read_cost, write_cost = write_optimized(r,w)
        costs[0][0].append(read_cost / N)
        costs[0][1].append(write_cost / N)
        costs[0][2].append((read_cost + write_cost)/ N)

        read_cost, write_cost = read_optimized(r,w)
        costs[1][0].append(read_cost / N)
        costs[1][1].append(write_cost / N)
        costs[1][2].append((read_cost + write_cost)/ N)

        read_cost, write_cost = intermediate(r,w)
        costs[2][0].append(read_cost / N)
        costs[2][1].append(write_cost / N)
        costs[2][2].append((read_cost + write_cost)/ N)

    titles = ['write-opt', 'read-opt', 'inter']
    for i in range(3):
        plt.figure(i)
        lines = []
        for j, cost in enumerate(costs[i]):
            line = plt.plot(x, cost, linestyles[i][j], label=labels[i][j])
            lines.append(line[0])

        #plt.ylim([0,400])
        plt.legend(lines, labels[i], loc='upper left', prop={'size':10})
        plt.ylabel('# page accesses')
        plt.xlabel('# reads out of 10 queries')
        plt.savefig('worst_case_' + titles[i] + '.png')

# Single read/write
def single_model():
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
    plt.savefig('single_model.png')

single_model()
worst_case_model()
