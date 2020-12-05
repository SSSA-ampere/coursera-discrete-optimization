#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import math
#import utils.tree_plot

class Input_Item:
    def __init__(self, index, value, weight):
        # input data index
        self.index = index
        # item value
        self.value = value
        # item weight
        self.weight  = weight

    def __str__(self):
        return '<%d, %d, %d>' % (self.index, self.value, self.weight)

class Tree_Node:
    def __init__(self):
        self.left = None
        self.right = None
        # unique node tree ID. used for plotting
        self.nodeid = 0
        # depth of the node in the tree
        self.tree_depth = 0
        # input data index
        self.index = 0
        # value obtained
        self.value = 0
        # room left
        self.room  = 0
        # current estimate
        self.estimate = 0

    def __str__(self):
        return '<%d, %d, %d, %d, %d>' % (self.tree_depth, self.index, self.value, self.room, self.estimate)


class Tree:
    #def __init__(self, items, sort_items_function, capacity):
    def __init__(self, items, capacity):
        # use lifo.append to push and lifo.pop to pop from it in LIFO order
        self.lifo = []
        # a sorted list of items 
        #self.items = sort_items_function(items)
        self.items = items
        # trunk of the tree
        self.trunk = None
        # capacity
        self.k = capacity
        # best value so far
        self.best_value = 0
        self.solution = [0]*len(items)
        # list of edges used for plotting the tree
        self.edge_list = []
    
    def __newItem__(self, item, estimate):
        return self.treeItem(item.index, item.value, item.weight, estimate)

    def transverse(self, estimate):
        # set the trunk 
        self.trunk = Tree_Node()
        self.trunk.tree_depth = 0
        self.trunk.index = 0
        self.trunk.nodeid = 0
        self.trunk.value = 0
        self.trunk.room = self.k
        self.trunk.estimate = estimate
        #self.trunk = self.treeItem(self.items[0].index, self.items[0].value, self.items[0].weight, estimate)
        # initialize the lifo
        self.lifo.append(self.trunk)
        # temporary solution
        temp_solution = [-1]*len(self.items)
        # node id used for plotting
        last_new_node = 0
        # points to the current input item of the input list
        input_idx = 0

        iter = 0
        # repeat until there is no item left or lifo is empty
        while (len(self.lifo) > 0):
            
            if self.lifo[0].left != None and self.lifo[0].right != None:
                # this node has been visited in both sides. drop it
                temp_solution[self.lifo[0].tree_depth] = -1
                self.lifo.pop(0)
                continue
            if input_idx >=  len(self.items):
                # return to the last valid value
                input_idx = self.lifo[0].tree_depth -1
                # tested all the inputs and none of them were good. Then, give it up and roolback
                if self.lifo[0].right == None:
                    self.lifo[0].right = -1
            # never gets negative
            input_idx = max(0,input_idx)
            # add another branch to the tree based on the next item of the input list
            iitem = self.items[input_idx]
            titem = Tree_Node()
            titem.index = iitem.index
            titem.tree_depth = input_idx+1
            # since the right side is checkd 1st in this if, it will have priority over the left side
            if self.lifo[0].right == None:
                titem.value = self.lifo[0].value+iitem.value
                titem.room = self.lifo[0].room-iitem.weight
                titem.estimate = self.lifo[0].estimate
                self.lifo[0].right = titem
            else:
                titem.value = self.lifo[0].value
                titem.room = self.lifo[0].room
                titem.estimate = self.lifo[0].estimate-iitem.value
                self.lifo[0].left = titem
                
            
            # if the estimate is better than the best value found so far,
            # then there is no need to continue searching this branch. 
            if titem.estimate > self.best_value:
                # if the new item fits in the bag, then it can be included into the tree
                if titem.room >=0:
                    if self.lifo[0].left == None:
                        temp_solution[self.lifo[0].tree_depth] = titem.index
                    else:
                        temp_solution[self.lifo[0].tree_depth] = -1

                    # Is the newly accepted node has a better value than the best value found so far ?
                    if titem.value > self.best_value:
                        self.solution = temp_solution.copy()
                        self.best_value = titem.value
                    # a new node is being created, then it needs a new ID
                    last_new_node +=1
                    titem.nodeid = last_new_node
                    edge = (self.lifo[0].nodeid, titem.nodeid)
                    self.edge_list.append(edge)
                    # insert the new item into in front of the LIFO
                    input_idx +=1
                    self.lifo.insert(0,titem)
                else:
                    input_idx +=1
                    self.lifo[0].right = None
            # if it does not fit anymore, ignore the new node
            else:
                # if the left is still None, then the current node was assigned to the right
                if self.lifo[0].left == None:
                    self.lifo[0].right = -1
                else:
                    self.lifo[0].left = -1
                    temp_solution[self.lifo[0].tree_depth] = -1
                    # both sides have been tested, then 
                    self.lifo.pop(0)
                    if len(self.lifo) > 0 :
                        input_idx = self.lifo[0].tree_depth -1

            iter += 1
        return iter

def max_tree_size(N):
    return 2**(N+1) - 1

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
        




def solve_it(input_data):
    # Depth first Branch & Bound with ...

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    items_removed = 0
    taken = [0]*item_count

    for i in range(item_count):
        line = lines[i+1]
        parts = line.split()
        # drop the single items that are bigger than the capacity
        # no need to insert these items in the search
        if int(parts[1]) <= capacity:
            items.append(Input_Item(i, int(parts[0]), int(parts[1])))
        else:
            items_removed += 1

    item_count -= items_removed

    # items sorted in reverse order of value/weight ratio
    items = sorted(items, key=lambda x: float(x.value/float(x.weight)))[::-1]
    # apply the linear_relaxation to get the BB estimate
    estimate = linear_relaxation(items,capacity)

    print ("Capacity %d, #items %d, estimate %.4f" % (capacity, item_count, estimate))
    print (", ".join(str(i) for i in items))

    #searching ...
    tree = Tree(items, capacity)
    iters = tree.transverse(estimate)

    #print the edge list
    print (tree.edge_list)
    print ("")

    # solution
    print ("Best value is", tree.best_value, "for items", tree.solution)
    print ("Solution found in iteration %d out of %d. %.6f%% of the tree transversed." % (iters,  max_tree_size(item_count), float(iters) / float(max_tree_size(item_count))))

    sum_value = 0
    sum_weight = 0
    print ("")
    print("_______________________________")
    print(' {:10s} {:10s} {:10s} '.format("Index","Value","Weight"))
    print("_______________________________")
    for i in tree.solution:
        if i >= 0:
            for j in items:
                if i == j.index:
                    print(' {:5d} {:10d} {:10d} '.format(j.index, j.value, j.weight))
                    sum_value += j.value
                    sum_weight += j.weight
    print("_______________________________")
    print(' {:16d} {:10d} '.format(sum_value, sum_weight))
    print ("")

    weight_slack = capacity - sum_weight
    for j in items:
        if j.weight <= weight_slack:
            print ("OOOOPS: With weight slack of ", weight_slack, "item", j, "should have been selected. check your algorithm!!!")

    # copy data to the expected output variables
    for i in tree.solution:
        if i >=0:
            taken[i] = 1
    value = tree.best_value

   
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

