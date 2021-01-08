#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

""" Solution to the 0-1 knapsack problem using branch and bound.

    It's a depth first Branch & Bound using stack-based search.
    This is a implementation of the Horowitz-Sahni for the 0-1 knapsack problem.
    See sec 2.5.1 of "Martello, S. & Toth, P. Knapsack problems: algorithms and 
    computer implementations. John Wiley & Sons, 1990" for more details.

    TODO:

        * Implement bound described in eq 2.19 and 2.20 of "Martello, S. & Toth, P. Knapsack problems: 
        algorithms and computer implementations. John Wiley & Sons, 1990".
        * Reimplement the algorithm more in the style of Sec 2.5.1 Horowitz-Sahni Algorithm.
        * Implement the algorithm more in the style of Sec 2.5.2 Martello-Toth Algorithm.

"""

import time # used for performance measurements
import networkx as nx # used only to save the tree
import math # used only for the trunc

# profiled with
# https://github.com/benfred/py-spy
# https://github.com/jlfwong/speedscope
# other possible profiler
# https://github.com/nvdv/vprof

# assign False to submit the solution
debug = True

# Assign True to build a Networkx graph of the tree and, at the end, save it in Pickle format
build_tree = True

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
        # used as unique identified when build_tree is True
        self.iter = 0
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
        # the node index of the best value. used only to paint this node with a diff color
        self.solution_idx = 0
        # expansion size
        self.iters = 0


    def relaxation(self, items, cur_estimate, slack_idx, slack_used, ritem_idx):
        """ Fractional item relaxation heuristic. This function is NOT WORKING !!!

        The explanation of the Fractional item relaxation heuristic in the video 'Knapsack 5 - relaxation, branch and bound',
        SUCK ... a big time !!!!
        In `this post <https://www.coursera.org/learn/discrete-optimization/discussions/weeks/2/threads/M30RzDnzEeew7Q7A7m3f-g/replies/OnqPNTqYEeerRhI_jX3yNA/comments/KrEW5z0xEee7bwpYS6iFWg>_` 
        has a descent explanation about the 77 estimate in the Coursera video.
        Also, the fractional heuristic is better explained in this `video <https://youtu.be/vb0juybGIKY?list=PL6KMWPQP_DM8t5pQmuLlarpmVc47DVXWd&t=264>_`.
        According to this video, it's possible to reduce the average execution time of the relaxation function.

        The idea of this optimization is that relaxation could be calculated incremently in a given path. 
        The estimate value of the next not taken item uses the prior node estimate. The worst case complexity is still O(n),
        but in average is O(1). However, this is quite complex for the data structure i have selected and it's full of corner cases that eventually 
        break the code. This optimization is mentioned in this `video <https://youtu.be/jxGwFWeZB0U?list=PL6KMWPQP_DM8t5pQmuLlarpmVc47DVXWd&t=3099>_`.

        Args:
            items ([Input_Item]): List of input items.
            cur_estimate (int): Current estimate.
            slack_idx (int): Slack item index.
            slack_used (int): The used slack.
            ritem_idx (int): The item to be excluded from the list.

        Returns:
            int, int, int: The new estimate, the new critical item index, the used part of the critical item (residual capacity).
        """
        room = 0
        estimate = 0
        item = 0
        removed_item = items[ritem_idx]
        if ritem_idx == slack_idx:
            # if the item to be deleted is the current critical item, then it's necessary
            # to be aware that this item was not entirely taken
            estimate = cur_estimate - math.trunc(slack_used * removed_item.value / removed_item.weight)
            room = slack_used
        else:
            # the item to be deleted was entire taken
            estimate = cur_estimate - removed_item.value
            room = removed_item.weight
        # defining the initial item to search the new critical item is the hardst part.
        # not fully understood yet 
        item = min(slack_idx + 1,len(items))
        # so that it will start searching from 'slack_idx' instead of from the beginning
        # reducing drastically the relaxation search time
        fractional = False
        # keep reducing the room until the next fraction item or the end of the list is found 
        while room > 0 and item < len(items):
            if room-items[item].weight >= 0:
                room -= items[item].weight
                slack_used = items[item].weight
                estimate += items[item].value
                item +=1
            else:
                slack_used = room
                room = room / float(items[item].weight)
                estimate += math.trunc(room * items[item].value)
                item -= 1
                fractional = True
                break
        if not fractional:
            item -= 1        

        return estimate, item, slack_used        


    def relax_martello_and_toth(self):
        """ A better upper bound compared to 'Dantzig's bound'. TO BE DONE!

        Bound taken from "Martello, S. & Toth, P. Knapsack problems: algorithms and 
        computer implementations. John Wiley & Sons, 1990", Section 2.3.1, eq 2.14 to 2.16.
        In the same section, eq 2.19 and 2.20, there is a even better bound. However, this 
        was not implemented. Left for future work.

        .. math::

            U_0 = \sum_{j=1}^{s-1} p_j + \left \lfloor \bar{c}\frac{p_{s+1}}{w_{s+1}} \right \rfloor
            U_1 = \sum_{j=1}^{s-1} p_j + \left \lfloor p_s - (w_s - \bar{c}) \frac{p_{s-1}}{w_{s-1}} \right \rfloor
            U_2 = \textsl{max}(U_0 \cdot U_1)

        """
        pass

    def linear_relaxation(self, items, capacity):
        """ Compute an upper bound for the cost. 
        
        THIS IS WORKING, BUT IT's SLOWER THAN THE CURRENT SOLUTION.
        It assumes that the items can be partitioned (fractioned).
        The slack item is the item which is fractioned.
        This relaxation method is also called 'Dantzig's bound'. 
        See Martello and Toth, 1990, Section 2.2.
        The item that is fractioned (does not fit entirely in the knapsack) is also called
        'critical item'. The weight used by the critical item is called 'residual capacity'.

        .. math::

            U_0 = \sum_{j=1}^{s-1} p_j + \left \lfloor \bar{c}\frac{p_{s}}{w_{s}} \right \rfloor

        Args:
            items ([Input_Item]): List of input items.
            capacity (int): Knapsack capacity.

        Returns:
            int, int, int: A tupple with : the estimated cost, the index of the critical item, and the residual capacity.
        """
        room = capacity
        item = 0
        slack_used = 0
        estimate = 0
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
                # trunc is applied because the estimate because the solution must be integer.
                # this might prune the search tree in some cases, but it increases execution time
                estimate += math.trunc(room * items[item].value)
                #estimate += room * items[item].value
                fractional = True
                break
            item +=1
        if not fractional:
            item -= 1
        return estimate,item,slack_used
    
    def transverse(self, estimate, slack_idx, slack_used):
        """ Main search function for the 0-1 knapsack problem.

        Args:
            estimate (int): The initial relaxation estimate.
            slack_idx (int): The index to the critical item.
            slack_used (int): The residual capacity.

        Returns:
            bool: False if the procedure was not aborted, meaning that the result is optimal.
        """
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
        # points to the current input item of the input list
        input_idx = 0
        # to avoid calling len multiple times inside the main loop
        items_lenght = len(self.items)
        # extract the max heap size. Used as a kind of memory used indicator
        #max_heap = 0
        # used as a kind of performance metric. number of expansions in the search
        iter = 1
        # % of knapsack filled. this is used as a stop criteria
        knapsack_utilization = 0.0
        # profiling vars
        #time_left_prep = 0
        #time_left_relax = 0
        #time_left_relax2 = 0
        # starting the execution timer
        start_time = time.time()
        abort = False
        # used only to save the tree
        G = None
        if build_tree:
            G = nx.DiGraph()
            G.add_node(0)
            G.nodes[0]['value'] = initial.value
            G.nodes[0]['estimate'] = initial.estimate
            G.nodes[0]['room'] = initial.room
            G.nodes[0]['color'] = 'gray'


        # THE STOP CRITERIA:
        # If program has run for at least MIM_EXEC_TIME and got at least
        # KNAP_TARGET_UTILIZATION knapsack utilization, then it can be stoped.
        # Morever, if the execution time is more than MAX_EXEC_TIME, no matter the 
        # KNAP_TARGET_UTILIZATION, it must also be stoped.

        # stop when the knapsack reaches 99.5% of utilization
        KNAP_TARGET_UTILIZATION = 0.995
        # minimum execution time. the execution cannot be aborted before this time (s)
        MIN_EXEC_TIME = 1 * 60
        # max execution time. the execution cannot run for more than this time (s)
        MAX_EXEC_TIME = 5 * 60

        # repeat until the stack is empty
        while (len(self.lifo) > 0 and not abort):
            input_idx = self.lifo[0].heap_depth
            # add another branch to the search based on the next item of the input list
            iitem = self.items[input_idx]
            titem = Heap_Node()
            titem.index = iitem.index
            # this can potentially leak the input list, but this is fixed with the 'min' few line below
            titem.heap_depth = input_idx+1
            # measure the time to execute this list copy 
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
                #tstart = time.time()
                titem.value = self.lifo[0].value
                titem.room = self.lifo[0].room
                deleted_idx = 0
                idx = 0
                room = self.capacity
                slack_used = 0
                estimate = 0                        
                for item in titem.taken_itens:
                    # when taking the left side, the item 'iitem' must be removed.
                    # Then, find the item and delete it
                    if item.index == iitem.index:
                        deleted_idx = idx
                    else:
                        if room-item.weight >= 0:
                            room -= item.weight
                            slack_used = item.weight
                            estimate += item.value
                            idx +=1
                        elif room > 0:
                            # print ("\n\nINTEGRAL PART:")
                            # print (" - prev estimate:",self.lifo[0].estimate)
                            # print (" - prev slack used:",self.lifo[0].slack_used)
                            # print (" - int estimate:", estimate)
                            # print (" - room:", room)
                            # print (" - used capacity:", self.capacity-room)
                            # print (str([str(i) for i in titem.taken_itens]))

                            slack_used = room
                            room = 0
                            used_fraction = slack_used / float(item.weight)
                            # trunc is applied because the estimate because the solution must be integer.
                            # this might prune the search tree in some cases, but it increases execution time
                            estimate += math.trunc(used_fraction * item.value)

                            # print ("FRACTIONAL PART:")
                            # print (" - deleted item idx:", deleted_idx)
                            # print (" - deleted item:", str(titem.taken_itens[deleted_idx]))
                            # print (" - critical item idx:", idx)
                            # print (" - critical item", str(item))
                            # print (" - frac estimate:", math.trunc(used_fraction * item.value))
                            # print (" - used slack:", slack_used)
                            # print (" - total estimate:", estimate)
                            #print (" - int+frac capacity:", self.capacity-slack_used)
                            break
                del (titem.taken_itens[deleted_idx]) 
                # print (str([str(i) for i in titem.taken_itens]))                  
                #time_left_prep += time.time()-tstart

                # ALTERNATE RELAXATION !!! This one works, but it is slower than the current code
                #tstart = time.time()
                #titem.estimate, titem.slack_idx, titem.slack_used =  self.linear_relaxation(titem.taken_itens,self.capacity)
                #time_left_relax += time.time()-tstart

                # ALTERNATE RELAXATION !!! This one DOES NOT WORK. It should be even faster than the current code
                # tstart = time.time()
                #estimate2, slack_idx2, slack_used2 =  self.relaxation(self.lifo[0].taken_itens, self.lifo[0].estimate, self.lifo[0].slack_idx, self.lifo[0].slack_used, deleted_idx)
                #estimate2, slack_idx2, slack_used2 =  estimate, idx, slack_used
                titem.estimate, titem.slack_idx, titem.slack_used =  estimate, idx, slack_used
                # time_left_relax2 += time.time()-tstart

                # UNCOMMENT THIS BLOCK TO TEST ALTERNATE RELAXATIONS STRATEGIES
                # if estimate2 != titem.estimate or slack_idx2 != titem.slack_idx and slack_used2 != titem.slack_used:
                #     print ("BUUUUUUUG !!!!! new relaxation is buggy !")
                #     print ('EXPECTED:', titem.estimate, titem.slack_idx, titem.slack_used)
                #     print ('PARENT:')
                #     taken = [0]*items_lenght
                #     for i in self.lifo[0].taken_itens:
                #         taken[i.index] = 1
                #     print (taken)
                #     print (self.lifo[0].estimate,self.lifo[0].value, self.lifo[0].room, self.lifo[0].slack_idx, self.lifo[0].slack_used)
                #     print ('GOT:')
                #     taken = [0]*items_lenght
                #     for i in titem.taken_itens:
                #         taken[i.index] = 1
                #     print (taken)
                #     print (self.lifo[0].estimate, self.lifo[0].slack_idx, self.lifo[0].slack_used, input_idx-1)
                #     print (estimate2, slack_idx2, slack_used2)
                self.lifo[0].left = 1
            
            # used only to save the tree format
            titem.iter  = iter
            if build_tree:
                G.add_node(titem.iter)
                G.add_edge(self.lifo[0].iter, titem.iter)
                G.nodes[titem.iter]['value'] = titem.value
                G.nodes[titem.iter]['estimate'] = titem.estimate
                G.nodes[titem.iter]['room'] = titem.room
                G.nodes[titem.iter]['color'] = 'gray'

            # if the estimate is better than the best value found so far,
            # then it is necessary to continue the search. 
            # if the new item fits in the bag, then it can be included into the tree
            if titem.estimate > self.best_value and titem.room >=0:
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
                    # used only to save the tree
                    self.solution_idx = iter
                    knapsack_utilization = sum([i.weight for i in self.solution]) / self.capacity
                    if build_tree:
                        G.nodes[titem.iter]['color'] = 'yellow'
                    if debug:
                        taken = [0]*items_lenght
                        for i in self.solution:
                            taken[i.index] = 1
                        print (" - BEST VALUE:", iter, self.best_value, taken)
                else:
                    # insert the new item into in front of the LIFO
                    self.lifo.insert(0,titem)
            # if the estimate is worst than the best value found so far,
            # then there is no need to continue searching this branch. 
            else:
                G.nodes[titem.iter]['color'] = 'aquamarine'
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
            # print the # of iterations every 2^19 and check the abortion criteria
            if iter % 0x80000 == 0:
                if debug:
                    print (' - iteration:',iter, ', best value:', self.best_value)
                cur_time = time.time()
                if (cur_time - start_time) > MIN_EXEC_TIME and knapsack_utilization > KNAP_TARGET_UTILIZATION:
                    abort = True
                if (cur_time - start_time) > MAX_EXEC_TIME:
                    abort = True

        if build_tree:
            G.nodes[self.solution_idx]['color'] = 'red'
            nx.write_gpickle(G,'tree.pickle')
            print ("tree has", G.number_of_nodes(), "nodes")
        self.iters = iter
        return abort

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
    """ Depth first Branch & Bound using stack (LIFO) search.

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
                items.append(Input_Item(i, int(parts[0]), int(parts[1])))
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

    tree = Heap(items, capacity)
    # apply the linear_relaxation to get the inital BB estimate
    estimate, slack_idx, slack_used = tree.linear_relaxation(items,capacity)
    if debug:
        print ("Capacity: %d, #items: %d, estimated value: %d" % (capacity, item_count, estimate))

    aborted = False
    if slack_used == items[slack_idx].weight:
        # this means that there is no fractioned item, so this is the optimal solution
        pass
    else:
        if debug:
            print ("\nSearching ...")
        aborted = tree.transverse(estimate, slack_idx, slack_used)

    if debug:
        print ("Performance metrics:")
        print (" - best value: ", tree.best_value)
        print (" - #iterations: ", tree.iters)
        print ("Solution:")
        sum_weight = print_table(tree.solution)
        print ("Knapsack with %.6f%% of occupation\n" % (sum_weight/capacity*100.0))
        weight_slack = capacity - sum_weight
        # create a list of indexes of all non selected items
        selected_idx = [i.index for i in tree.solution] 
        # search for excluded items with lower weight than the weight_slack
        for j in items:
            # ks_500_0, item 51 has weight 1 and value == 0!
            if j.weight <= weight_slack and j.value >0:
                if j.index not in selected_idx:
                    print ("OOOOPS: With weight slack of", weight_slack, ", item", j.index, "with weight", j.weight, "should have been selected. check your algorithm!!!")

    # copy data to the expected output variables
    for i in tree.solution:
        taken[i.index] = 1
    value = tree.best_value

    # say if the solution is optimal or not. If it is abborted, then there is no 
    # garantee that this is an optimal solution
    if aborted:
        optimal = 0
    else:
        optimal = 1
    # prepare the solution in the specified output format
    output_data = str(int(value)) + ' ' + str(optimal) + '\n'
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
