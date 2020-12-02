#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        # input data index
        self.index = 0
        # value obtained
        self.value = 0
        # room left
        self.room  = 0
        # current estimate
        self.estimate = 0

    def __str__(self):
        return '<%d, %d, %d, %d>' % (self.index, self.value, self.room, self.estimate)

    def fillItem(self, item, estimate):
        self.index = item.index
        self.value = item.value
        self.room  = item.weight
        self.estimate = estimate

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
        #self.best_index = 0
        # items in each tree node
        #self.treeItem = namedtuple("Item", ['index', 'value', 'room', 'estimate'])
    
    def __newItem__(self, item, estimate):
        return self.treeItem(item.index, item.value, item.weight, estimate)

    def transverse(self, estimate):
        # set the trunk 
        self.trunk = Tree_Node()
        self.trunk.index = 0
        self.trunk.value = 0
        self.trunk.room = self.k
        self.trunk.estimate = estimate
        #self.trunk = self.treeItem(self.items[0].index, self.items[0].value, self.items[0].weight, estimate)
        # initialize the lifo
        self.lifo.append(self.trunk)
        #self.lifo[0].value +=1
        #print ("val:", self.trunk.value, self.lifo[0].value)

        iter = 0
        # repeat until there is no item left or lifo is empty
        while (len(self.lifo) > 0):
            
            # add another branch to the tree based on the next item of the input list
            iitem = self.items[self.lifo[0].index]
            # if there is enough capacity and 
            
            # then accept the item.
            # the tree item (titem) has:
            #   value: the current tree item + the next new item
            #   room: is the current tree item room - the room required by the new item
            #   estimate:  is the same estimate as the current tree item estimate
            titem = Tree_Node()
            titem.index = iitem.index
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
            # if the new item fits in the bag and its estimate is better than the best value found so far,
            # then the new node is accepted into the tree
            if titem.room >=0  and titem.estimate > self.best_value:
                # Is the newly accepted node has a better value than the best value found so far ?
                if titem.value > self.best_value:
                    self.best_value = titem.value
                # insert the new item into in front of the LIFO
                self.lifo.insert(0,titem)
            # if it does not fit anymore, ignore the new node
            else:
                # if the left is still None, then the current node was assigned to the right
                if self.lifo[0].left == None:
                    self.lifo[0].right = -1
                else:
                    self.lifo[0].left = -1

            iter += 1

        




def solve_it(input_data):
    # Depth first Branch & Bound with ...

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(item_count):
        line = lines[i+1]
        parts = line.split()
        items.append(Input_Item(i, int(parts[0]), int(parts[1])))

    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    # items sorted in rever order of value/weight ratio
    items = sorted(items, key=lambda x: float(x.value/float(x.weight)))[::-1]
    print (", ".join(str(i) for i in items))
    tree = Tree(items, capacity)
    #tree.transverse(30)



    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    
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

