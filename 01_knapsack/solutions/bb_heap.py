#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import time

# assign False to submit the solution
debug = True

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
        # where None means not visited, -1 visited but without solution, 1 already visited
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
        # index to the fractioned item in self.items
        self.slack_idx = 0
        # e.g. if the slack item has weight 5, but only 3 was used, then slack_used is 3
        self.slack_used = 0
        # current taken itens
        self.taken_itens = []

    def __str__(self):
        return '<%d, %d, %d, %d, %.2f, %d, %d, %s>' % (self.heap_depth, self.index, 
            int(self.value), self.room, self.estimate, self.slack_idx, self.slack_used,
            str(self.taken_itens))


class Heap:
    #def __init__(self, items, sort_items_function, capacity):
    def __init__(self, items, capacity):
        # use lifo.insert(0,) to push and lifo.pop(0) to pop from it in LIFO order
        self.lifo = []
        # a sorted list of items 
        self.items = items
        self.item_len = len(items)
        self.capacity = capacity
        # best value so far
        self.best_value = 0
        # holds a list with selected item indexes 
        self.solution = [0]*len(items)
        # expansion size
        self.iters = 0

    def relaxation(self, cur_estimate, slack_idx, slack_used, weight):
        """ Fractional item relaxation heuristic.

        The explanation of the Fractional item relaxation heuristic in the video 'Knapsack 5 - relaxation, branch and bound',
        SUCK ... a big time !!!!
        In `this post <https://www.coursera.org/learn/discrete-optimization/discussions/weeks/2/threads/M30RzDnzEeew7Q7A7m3f-g/replies/OnqPNTqYEeerRhI_jX3yNA/comments/KrEW5z0xEee7bwpYS6iFWg>_` 
        has a descent explanation about the 77 estimate than the Coursera video.
        Also, the fractional heuristic is better explained in this `video <https://youtu.be/vb0juybGIKY?list=PL6KMWPQP_DM8t5pQmuLlarpmVc47DVXWd&t=264>_`.

        Args:
            cur_estimate (float): Current estimate.
            slack_idx (int): Slack item index.
            slack_used (int): The used slack.
            weight (float): The available weight.

        Returns:
            float, int, int: The new estimate, the new slack item index, the used part of the slack item.
        """

        # debug check
        #if slack_used < 1:
        #    print ("BUUUUUUUG! slack must be >=1 ")
        #    sys.exit(1)
        # use the rest of the fractioned item
        weight = weight - (self.items[slack_idx].weight - slack_used)
        estimate = cur_estimate + (self.items[slack_idx].value * (float(slack_used) / float(self.items[slack_idx].weight)))
        item = slack_idx + 1 
        # keep reducing the weight until the next fraction item or the end of the list is found 
        while weight > 0 and item < self.item_len:
            if weight-self.items[item].weight >= 0:
                # integral item found
                weight -= self.items[item].weight
                slack_used = self.items[item].weight
                estimate += self.items[item].value
            else:
                # fractioned item found
                slack_used = weight
                weight = weight / float(self.items[item].weight)
                estimate += weight * self.items[item].value
                break
            item +=1
        return estimate, item, slack_used        


        # room = float(capacity)
        # item = 0
        # slack_used = 0
        # estimate = 0.0
        # while room > 0 and item < len(items):
        #     if room-items[item].weight >= 0:
        #         room -= items[item].weight
        #         slack_used = items[item].weight
        #         estimate += items[item].value
        #     else:
        #         slack_used = room
        #         room = room / float(items[item].weight)
        #         estimate += room * items[item].value
        #         break
        #     item +=1
        # return estimate,item,slack_used

    def linear_relaxation(self, items, capacity):
        """ Compute a upper bound for the cost.
        
        It assumes that the items can be partitioned (fractioned).
        The slack item is the item which is fractioned.

        Args:
            items ([Input_Item]): List of input items.
            capacity (int): Knapsack capacity.

        Returns:
            float, int, int: A tupple with : the estimated cost, the index of the slack item.
        """

        room = float(capacity)
        item = 0
        slack_used = 0
        estimate = 0.0
        fractional = False
        # I think that this condition cen be removed 'room > 0 and'
        while room > 0 and item < len(items):
            if room-items[item].weight >= 0:
                room -= items[item].weight
                slack_used = items[item].weight
                estimate += items[item].value
            else:
                slack_used = room
                room = room / float(items[item].weight)
                estimate += room * items[item].value
                fractional = True
                break
            item +=1
        if not fractional:
            item -= 1
        return estimate,item,slack_used
    
    def transverse(self, estimate, slack_idx, slack_used):
        # set the initial node for heap searching
        initial = Heap_Node()
        initial.heap_depth = 0
        initial.index = 0
        initial.value = 0
        initial.room = self.capacity
        initial.estimate = estimate
        initial.slack_idx = slack_idx
        initial.slack_used = slack_used
        initial.taken_itens = self.items[:]
        # initialize the lifo
        self.lifo.append(initial)
        # temporary solution
        #temp_solution = [-1]*len(self.items)
        # points to the current input item of the input list
        input_idx = 0
        # to avoid calling len multiple times inside the main loop
        items_lenght = len(self.items)
        # extract the max heap size. Used as a kind of memory used indicator
        max_heap = 0
        # used as a kind of performance metric. number of expansions in the search
        iter = 0
        # profiling vars
        time_left_prep = 0
        time_left_relax = 0
        time_copy = 0
        # repeat until the LIFO is empty
        while (len(self.lifo) > 0):
            #if iter == 55000000:
            #    print ("AM I STUCK ?!?!?")
                #sys.exit(1)
            input_idx = self.lifo[0].heap_depth
            # add another branch to the search based on the next item of the input list
            iitem = self.items[input_idx]
            titem = Heap_Node()
            titem.index = iitem.index
            # this can potentially leak the input list, but this is fixed with the 'min' few line below
            titem.heap_depth = input_idx+1
            # the copy has been moved to the inner 'ifs' to reduce the # times this ops is executed
            #tstart = time.time()
            titem.taken_itens = self.lifo[0].taken_itens[:]
            #time_copy += time.time() - tstart
            # since the right side is checked 1st in this if, it will have priority over the left side
            if self.lifo[0].right == None:
                titem.value = self.lifo[0].value+iitem.value
                titem.room = self.lifo[0].room-iitem.weight
                titem.estimate = self.lifo[0].estimate
                titem.slack_idx  = self.lifo[0].slack_idx
                titem.slack_used = self.lifo[0].slack_used
                self.lifo[0].right = 1
            else:
                # tstart = time.time()
                # titem.taken_itens = self.lifo[0].taken_itens[:]
                # time_copy += time.time() - tstart
                tstart = time.time()
                titem.value = self.lifo[0].value
                titem.room = self.lifo[0].room
                # when taking the left side, the item 'iitem' must be removed.
                # Then, find the item and delete it
                # if len(titem.taken_itens)==0:
                #     print ("MEEEEEGA PAU ! empty taken_itens")
                #     print ('IITEM:')
                #     print (iitem)
                #     print ('TITEM:')
                #     print (titem)
                #     sys.exit(1)
                # bug = True
                for idx, item  in enumerate(titem.taken_itens):
                    if item.index == iitem.index:
                        del (titem.taken_itens[idx])
                        # bug = False
                        break
                # if bug:
                #     print ("MEEEEEGA PAU ! iitem not found")
                #     print ('IITEM:')
                #     print (iitem)
                #     print ('TITEM:')
                #     print (titem)
                #     sys.exit(1)
                time_left_prep += time.time()-tstart
                tstart = time.time()
                titem.estimate, titem.slack_idx, titem.slack_used =  self.linear_relaxation(titem.taken_itens,self.capacity)
                time_left_relax += time.time()-tstart
                self.lifo[0].left = 1
            
            # if the estimate is better than the best value found so far,
            # then it is necessary to continue the search. 
            # if the new item fits in the bag, then it can be included into the tree
            if titem.estimate > self.best_value and titem.room >=0:
                # do costly operation as late as possible to remove it from the 'hot zone'
                # tstart = time.time()
                # if self.lifo[0].left == None:
                #     titem.taken_itens = self.lifo[0].taken_itens[:]
                # time_copy += time.time() - tstart



                # the correct would be to put the min after
                # titem.heap_depth = input_idx+1. However, most titem are ignored.
                # here is the place where titem is not ignored and it is saved.
                # then, it is safe to put the min here incurring in less overhead
                titem.heap_depth = min(titem.heap_depth,items_lenght-1)
                # a solution is only found at the 'leaf' of the fake tree
                # Is the newly accepted node has a better value than the best value found so far ?
                if input_idx == items_lenght-1 and titem.value > self.best_value:
                    self.solution = titem.taken_itens[:]
                    self.best_value = titem.value
                else:
                    # insert the new item into in front of the LIFO
                    self.lifo.insert(0,titem)
                # this is for debug only. the heap depth is not supposed to be > than the # of items
                # if max_heap < len(self.lifo):
                #     if max_heap < items_lenght:
                #         max_heap = len(self.items)
                #     else:
                #         print ("MEEEEEGA PAU ! max_heap > len(self.items)")
                #         print ('IITEM:')
                #         print (iitem)
                #         print ('TITEM:')
                #         print (titem)
                #         sys.exit(1)
            # if the estimate is worst than the best value found so far,
            # then there is no need to continue searching this branch. 
            else:
                # if the left is still None, then the current node was assigned to the right
                if self.lifo[0].left == None:
                    # it means end of the search via the right side, but the left side was not searched yet
                    self.lifo[0].right = -1
                else:
                    self.lifo[0].left = -1

            # this node has been visited in both sides. drop it until there is a node with a path not visited
            while len(self.lifo) > 0 and self.lifo[0].left != None and self.lifo[0].right != None:
                self.lifo.pop(0)
            iter += 1
            # print the # of iterations every 2^19
            if iter % 0x80000 == 0:
                print (' - iteration:',iter, ', best value:', self.best_value)
        print ("TIME prep:",time_left_prep,",TIME relax:",time_left_relax, 'TIME copy:', time_copy)
        self.iters = iter

def max_tree_size(N):
    """ Calculate the max size of a tree.

    Args:
        N (int): The tree depth.

    Returns:
        int: The number of nodes in the tree.
    """
    return 2**(N+1) - 1


        

def print_table(solution):
    sum_value = 0.0
    sum_weight = 0
    print("__________________________________")
    print(' {:>11s} {:>10s} {:>10s} '.format("Index","Value","Weight"))
    print("__________________________________")
    cnt=1
    for i in solution:
        print(' {:5d} {:5d} {:10d} {:10d} '.format(cnt, i.index, int(i.value), i.weight))
        sum_value += i.value
        sum_weight += i.weight
        cnt +=1
    print("__________________________________")
    print(' {:21d} {:10d} '.format(int(sum_value), sum_weight))
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
                #fake_solution.append(i)
            # if some weight is zero, then assign a very small value to avoid zero div exception
                
        else:
            items_removed += 1

    item_count -= items_removed

    if debug:
        print ("")
        print ("Input:")
        print_table(items)

    # items sorted in reverse order of value/weight ratio
    items = sorted(items, key=lambda x: float(x.value/float(x.weight)))[::-1]

    if debug:
        print ("")
        print ("Sorted:")
        print_table(items)

    #searching ...
    tree = Heap(items, capacity)
    # apply the linear_relaxation to get the BB estimate
    estimate, slack_idx, slack_used = tree.linear_relaxation(items,capacity)
    if debug:
        print ("Capacity: %d, #items: %d, estimated value: %.4f" % (capacity, item_count, estimate))

    print ("\nSearching ...")
    tree.transverse(estimate, slack_idx, slack_used)

    if debug:
        # solution
        #remove_minus1 = [i for i in tree.solution if i != -1] 
        #print ("Best value is", tree.best_value, "for items", remove_minus1)
        #print ("Solution found in iteration %d out of %d. %.6f%% of the tree transversed." % (iters,  max_tree_size(item_count), float(iters) / float(max_tree_size(item_count))))
        print ("Performance metrics:")
        print (" - best value: ", tree.best_value)
        print (" - #iterations: ", tree.iters)
        print ("Solution:")
        sum_weight = print_table(tree.solution)
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
        taken[i.index] = 1
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

