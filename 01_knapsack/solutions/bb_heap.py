#!/usr/bin/python3.6
# -*- coding: utf-8 -*-


# assign False to submit the solution
debug = False

class Input_Item:
    def __init__(self, index, value, weight):
        """ Item in the input list.

        Args:
            index (int): Index of the item in the original input list.
            value (float): Item value.
            weight (int): Item weight.
        """
        # input data index
        self.index = index
        # item value
        self.value = value
        # item weight
        self.weight  = weight

    def __str__(self):
        return '<%d, %d, %d>' % (self.index, int(self.value), self.weight)

class Heap_Node:
    def __init__(self):
        """ Item in the heap.

        """        
        # left and right have values: None, -1, and 1.
        # where None means not visited, -1 visited but without solution, 
        # 1 means visited with possible solution
        self.left = None
        self.right = None
        # depth of the node in the 'tree'
        self.heap_depth = 0
        # input data index
        self.index = 0
        # value obtained
        self.value = 0
        # room left
        self.room  = 0
        # current estimate
        self.estimate = 0

    def __str__(self):
        return '<%d, %d, %d, %d, %.2f>' % (self.heap_depth, self.index, int(self.value), self.room, self.estimate)


class Heap:
    #def __init__(self, items, sort_items_function, capacity):
    def __init__(self, items, capacity):
        # use lifo.insert(0,) to push and lifo.pop(0) to pop from it in LIFO order
        self.lifo = []
        # a sorted list of items 
        self.items = items
        # capacity
        self.k = capacity
        # best value so far
        self.best_value = 0
        # holds a list with selected item indexes 
        self.solution = [0]*len(items)
        
    
    def transverse(self, estimate):
        # set the initial node for heap searching
        initial = Heap_Node()
        initial.heap_depth = 0
        initial.index = 0
        initial.value = 0
        initial.room = self.k
        initial.estimate = estimate
        # initialize the lifo
        self.lifo.append(initial)
        # temporary solution
        temp_solution = [-1]*len(self.items)
        # points to the current input item of the input list
        input_idx = 0
        # to avoid calling len multiple times inside the main loop
        items_lenght = len(self.items)
        # extract the max heap size. Used as a kind of memory used indicator
        max_heap = 0
        # used as a kind of performance metric
        iter = 0
        # repeat until the LIFO is empty
        while (len(self.lifo) > 0):
            #if iter >= 20000:
            #    print ("AM I STUCK ?!?!?")
            if self.lifo[0].left != None and self.lifo[0].right != None:
                # this node has been visited in both sides. drop it
                temp_solution[self.lifo[0].heap_depth] = -1
                self.lifo.pop(0)
                continue
            if input_idx >=  items_lenght:
                # reaching the last item to be tested. return to the last valid value to continue the search
                input_idx = self.lifo[0].heap_depth -1
                # tested all the inputs and none of them were good. Then, give it up and roolback
                if self.lifo[0].right == None:
                    self.lifo[0].right = -1
            # never gets negative
            input_idx = max(0,input_idx)
            # add another branch to the search based on the next item of the input list
            iitem = self.items[input_idx]
            titem = Heap_Node()
            titem.index = iitem.index
            # this can potentially leak the input list, but this is fixed with the 'min' few line below
            titem.heap_depth = input_idx+1
            # since the right side is checkd 1st in this if, it will have priority over the left side
            if self.lifo[0].right == None:
                titem.value = self.lifo[0].value+iitem.value
                titem.room = self.lifo[0].room-iitem.weight
                titem.estimate = self.lifo[0].estimate
                self.lifo[0].right = 1
            else:
                titem.value = self.lifo[0].value
                titem.room = self.lifo[0].room
                titem.estimate = self.lifo[0].estimate-iitem.value
                self.lifo[0].left = 1
            
            # if the estimate is better than the best value found so far,
            # then it is necessary to continue the search. 
            if titem.estimate > self.best_value:
                # if the new item fits in the bag, then it can be included into the tree
                if titem.room >=0:
                    # the correct would be to put the min after
                    # titem.heap_depth = input_idx+1. However, most titem are ignored.
                    # here is the place where titem is not ignored and it is saved.
                    # then, it is safe to put the min here incurring in less overhead
                    titem.heap_depth = min(titem.heap_depth,items_lenght-1)
                    if self.lifo[0].left == None:
                        temp_solution[self.lifo[0].heap_depth] = titem.index
                    else:
                        temp_solution[self.lifo[0].heap_depth] = -1

                    # Is the newly accepted node has a better value than the best value found so far ?
                    if titem.value > self.best_value:
                        self.solution = temp_solution.copy()
                        self.best_value = titem.value
                    # insert the new item into in front of the LIFO
                    input_idx +=1
                    self.lifo.insert(0,titem)
                    # gather performance stats
                    if max_heap < len(self.lifo):
                        max_heap = len(self.lifo)
                # if it does not fit anymore, ignore the new node, but continue the search in this branch
                else:
                    input_idx +=1
                    self.lifo[0].right = None
            # if the estimate is worst than the best value found so far,
            # then there is no need to continue searching this branch. 
            else:
                # if the left is still None, then the current node was assigned to the right
                if self.lifo[0].left == None:
                    # it means end of the search via the right side, but the left side was not searched yet
                    self.lifo[0].right = -1
                else:
                    self.lifo[0].left = -1
                    temp_solution[self.lifo[0].heap_depth] = -1
                    # both sides have been tested, then drop this node from the LIFO
                    self.lifo.pop(0)
                    if len(self.lifo) > 0 :
                        input_idx = self.lifo[0].heap_depth -1

            iter += 1
        return (iter, max_heap)

def max_tree_size(N):
    """ Calculate the max size of a tree.

    Args:
        N (int): The tree depth.

    Returns:
        int: The number of nodes in the tree.
    """
    return 2**(N+1) - 1

def linear_relaxation(items, capacity):
    """ Compute a upper bound for the cost.
    
    It assumes that the items can be partitioned (fractioned).

    Args:
        items ([Input_Item]): List of input items.
        capacity (int): Knapsack capacity.

    Returns:
        float: The estimated cost.
    """

    room = float(capacity)
    item = 0
    estimate = 0.0
    while room > 0 and item < len(items):
        if room-items[item].weight >= 0:
            room -= items[item].weight
            estimate += items[item].value
        else:
            room = room / float(items[item].weight)
            estimate += room * items[item].value
            break
        item +=1
    return estimate
        

def print_table(items, solution):
    sum_value = 0.0
    sum_weight = 0
    print("_______________________________")
    print(' {:10s} {:10s} {:10s} '.format("Index","Value","Weight"))
    print("_______________________________")
    for i in items:
        if i.index in solution:
            print(' {:5d} {:10d} {:10d} '.format(i.index, int(i.value), i.weight))
            sum_value += i.value
            sum_weight += i.weight
    print("_______________________________")
    print(' {:16d} {:10d} '.format(int(sum_value), sum_weight))
    print ("") 
    return sum_weight


def solve_it(input_data):
    """ Depth first Branch & Bound using heap (LIFO) search.

    """
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []
    items_removed = 0
    taken = [0]*item_count

    fake_solution = []
    for i in range(item_count):
        line = lines[i+1]
        parts = line.split()
        # drop the single items that are bigger than the capacity
        # no need to insert these items in the search
        if int(parts[1]) <= capacity:
            # there are a couple of items with value zero. remove them because they dont 
            # help to improve the value metric
            if int(parts[0]) > 0:
                if int(parts[1]) <= 0:
                    print ("WOOHHH ! the list has a item with no weight !!!! it defies the laws of physics!!! ")
                    sys.exit(0)
                items.append(Input_Item(i, float(parts[0]), int(parts[1])))
                # this is used only in debug mode
                fake_solution.append(i)
            # if some weight is zero, then assign a very small value to avoid zero div exception
                
        else:
            items_removed += 1

    item_count -= items_removed

    if debug:
        print ("")
        print ("Input:")
        print_table(items,fake_solution)

    # items sorted in reverse order of value/weight ratio
    items = sorted(items, key=lambda x: float(x.value/float(x.weight)))[::-1]
    # apply the linear_relaxation to get the BB estimate
    estimate = linear_relaxation(items,capacity)

    if debug:
        print ("Capacity: %d, #items: %d, estimated value: %.4f" % (capacity, item_count, estimate))
        #print (", ".join(str(i) for i in items))

    #searching ...
    tree = Heap(items, capacity)
    (iters, max_heap) = tree.transverse(estimate)

    if debug:
        # solution
        #remove_minus1 = [i for i in tree.solution if i != -1] 
        #print ("Best value is", tree.best_value, "for items", remove_minus1)
        #print ("Solution found in iteration %d out of %d. %.6f%% of the tree transversed." % (iters,  max_tree_size(item_count), float(iters) / float(max_tree_size(item_count))))
        print ("Performance metrics:")
        print (" - #iterations: ", iters)
        print (" - max heap size: ", max_heap)
        print ("Solution:")
        sum_weight = print_table(items,tree.solution)
        print ("Knapsack with %.6f%% of occupation\n" % (sum_weight/capacity*100.0))
        weight_slack = capacity - sum_weight
        # create a list of indexes of all non selected items
        remove_minus1 = [i for i in tree.solution if i != -1] 
        excluded_items = list(set(remove_minus1)^set(range(item_count)))
        # search for excluded items with lower weight than the weight_slack
        for j in items:
            # ks_500_0, item 51 has weight 1 and value == 0!
            if j.weight <= weight_slack and j.value >0:
                if j.index in excluded_items:
                    print ("OOOOPS: With weight slack of", weight_slack, ", item", j.index, "with weight", j.weight, "should have been selected. check your algorithm!!!")

    # copy data to the expected output variables
    for i in tree.solution:
        if i >=0:
            taken[i] = 1
    value = tree.best_value

   
    # prepare the solution in the specified output format
    output_data = str(int(value)) + ' ' + str(0) + '\n'
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

