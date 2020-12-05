#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

# assign False to submit the solution
debug = False

def linear_relaxation(items, capacity):
    room = capacity
    item = 0
    estimate = 0.0
    while room > 0 and item < len(items):
        if room-items[item].weight >= 0:
            room -= items[item].weight
            estimate += items[item].value
        else:
            room = float(room) / float(items[item].weight)
            estimate += float(room) * items[item].value
            break
        item +=1
    return estimate

def print_table(items, taken):
    sum_value = 0
    sum_weight = 0
    print("_______________________________")
    print(' {:10s} {:10s} {:10s} '.format("Index","Value","Weight"))
    print("_______________________________")
    idx = 0
    for i in items:
        if taken[idx] == 1:
            print(' {:5d} {:10d} {:10d} '.format(i.index, i.value, i.weight))
            sum_value += i.value
            sum_weight += i.weight
        idx +=1
    print("_______________________________")
    print(' {:16d} {:10d} '.format(sum_value, sum_weight))
    print ("")

    return sum_weight


def solve_it(input_data):
    """ sort items in reverse order of value/weight ratio.

    """

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    if debug:
        print ("")
        print ("Capacity: %d, #items: %d" % (capacity, item_count))
        print ("Input:")
        print_table(items, [1]*item_count)


    # items sorted in reverse order of value/weight ratio
    items = sorted(items, key=lambda x: float(x.value/float(x.weight)))[::-1]

    taken_debug = [0]*item_count
    idx = 0
    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            taken_debug[idx] = 1
            value += item.value
            weight += item.weight
        idx +=1
    
    if debug:
        print ("")
        estimate = linear_relaxation(items,capacity)
        print ("Estimated value: %.2f" % (estimate))
        #print (", ".join(str(i) for i in items))
        print ("")
        print ("Solution:")
        sum_weight = print_table(items, taken_debug)
        print ("Knapsack with %.6f%% of occupation\n" % (sum_weight/capacity))
        weight_slack = capacity - sum_weight
        idx=0
        for j in items:
            if taken_debug[idx] == 0 and j.weight <= weight_slack:
                print ("OOOOPS: With weight slack of", weight_slack, ", item", j, "with weight", items[j].weight, "should have been selected. check your algorithm!!!")
            idx +=1


    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

