#!/usr/bin/python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Andrea Rendl
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# -------------------------------------------------------------------------------
#     ABOUT THE MINIZINC SOLVER:
# -------------------------------------------------------------------------------
#
# ABOUT MINIZINC:
#
# Minizinc is a highlevel modelling language in which it is easy to formulate
# problems. A problem formulation consists of a problem model (.mzn file) 
# and a data file (.dzn file). Given a problem and a data file, the Minizinc tool
# can translate the problem into a MIP model or CP model and forwards it to a 
# solver. This is very convenient for the user, since she/he does not have to deal
# with the solver input format.
#
# ABOUT THIS SOLVER:
# 
# The problem model for the set covering problem can be found in the file 
# 'setCovering.mzn'. This script automatically generates the Minizinc data file 
# for a given problem instance, and writes it into the file 'data.dzn'. The two
# files are then forwarded to a MIP solver (CBC from COIN-OR) and solved. The 
# solver output is read and converted into the submission output format.
#
# -------------------------------------------------------------------------------
#    HOW TO USE THIS SOLVER:
# -------------------------------------------------------------------------------
# 
# + Download and install Minizinc: http://www.minizinc.org/
#
# + Make sure that the Minizinc binaries are part of your PATH. 
#   To achieve that, enter the following into your shell (or add it to your 
#   ~/.bashrc or equivalent):
#       export PATH=$PATH:/your/path/to/minizinc/bin/
# 
# + Execute the solver just like the standard solver. For instance:
#   python solver_minizinc.py data/sc_25_0
#
# + If you want to play around with the solver: 
#   + You can change the maximum number of solutions that the solver will search 
#     for in this script (search for 'nb_solutions').
#   + There are different kinds of solvers that you can use for solving 
#     the problem: a MIP solver and 3 different CP solvers. To play around with 
#     them, uncomment the right lines for invoking the Minizinc process (search 
#     for 'ALTERNATIVE' is this file).
#
# + There are many other Minizinc examples in the /examples directory of your
#   Minizinc installation.
# 
# -------------------------------------------------------------------------------
#    GETTING HELP
# -------------------------------------------------------------------------------
#
# + If you need any help, have a look at the Discussion forum of the course and
#   post your questions. Make sure that nobody has asked your question already!
#
# -------------------------------------------------------------------------------

# solver adapted to run minizinc
# https://github.com/discreteoptimization/setcover/blob/master/minizinc_001/solver.py

# Implemented simplifications
# - lb: run several cliques and get the longest one
# - ub: run several heuristics and get the one with the longest set of colors
# - remove nodes with degree == 1
# - set the colors of the maximal clique
# - symmetry breaking constraints in the model template
# - check for maximal independent set, nodes that only connect to the max clique 

# TODO:
# - other ways to reduce the problem size:
#   See the book 'A Guide to Graph Colouring: Algorithms and Applications', 
#   Sec. 3.3 Reducing Problem Size
# - improve the lower bound:
#   See the book 'A Guide to Graph Colouring: Algorithms and Applications', 
#   2.2.1 Lower Bounds
#   Let α(G) denote the independence number of a graph G, defined as the number of
#   vertices contained in the largest independent set in G . I
#   colors >= max(max clique size, ceil(n/max independent set size))
# - try this implementation rather than the ones in NetworkX
#   https://en.wikipedia.org/wiki/Independent_set_(graph_theory)#Maximum_independent_sets_and_maximum_cliques
#   https://igraph.org/python/doc/igraph.GraphBase-class.html#independent_vertex_sets
#   https://igraph.org/python/doc/igraph.GraphBase-class.html#maximal_cliques
#   https://igraph.org/python/doc/igraph.GraphBase-class.html#largest_cliques
#   https://doc.sagemath.org/html/en/reference/graphs/sage/graphs/graph_coloring.html
#   https://doc.sagemath.org/html/en/reference/graphs/sage/graphs/cliquer.html

import os, signal
from subprocess import Popen, PIPE, TimeoutExpired
import networkx as nx
from networkx.algorithms.approximation import clique
import matplotlib.pyplot as plt 
import random
import statistics
#import time
from nxviz.plots import MatrixPlot


# TODO: usar Matrix plot p grafos grandes
# https://nxviz.readthedocs.io/en/latest/usage.html#matrix-plots
# https://www.geeksforgeeks.org/exploring-correlation-in-python/
# https://py3plex.readthedocs.io/en/latest/supra.html

# TODO olhar https://stackoverflow.com/questions/62502906/how-to-improve-the-performance-of-my-graph-coloring-model-in-minizinc
# https://ozgurakgun.github.io/ModRef2017/files/ModRef2017_SolutionCheckingWithMinizinc.pdf
# https://stackoverflow.com/questions/45536579/optimization-of-minizinc-model

DEBUG = True

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    node_count = int(parts[0])
    edge_count = int(parts[1])
    
    edges = []
    for i in range(1, edge_count+1):
        parts = lines[i].split()
        edges.append((int(parts[0]), int(parts[1])))

    # generate NetworkX graph
    original_num_nodes, G = nxGraph(edges)

    # get the cliques used next
    max_clique, cliques = get_cliques(G)

    # olhar: networkx.maximal_independent_set()

    #  value x of the maximal clique can
    # be used to reduce the graph size by removing every
    # vertex that has a degree smaller than x − 1.

    # the max_clique is the lower bound. at least this number of colors are required
    lb = len(max_clique)
        
    # run the upper bound
    real_ub, ub = upper_bound(G)
    if DEBUG:
        print ('lb:', lb)
        print ('ub:', ub)
        print ('max_degree:', real_ub)

    # generate the minizinc model with additional custom contraints
    new_model_lines = []
    j = 0
    for n in max_clique:
        new_model_lines.append('constraint colors[%d] = %d;' % (n,j+1))
        j +=1    
    gen_model(G, new_model_lines,'graphColoring-template.mzn', 'graphColoring.mzn')
    #gen_model2(G)
    #gen_model3(G)

    #ub = lb
    #lb = ub
    # it will reducing the upper bound until it cannot find a solution in time
    best_ub = 100000
    # these are the partial solutions
    colors = 0
    solution = []
    timeout = 60*5

    # the states are 'timeout', 'nsat', 'sat'
    minizinc_state = None
    # set variables for process communication with minizinc
    stdout = None
    stderr = None
    while True:
        if DEBUG:
            print ("running with lb:", lb, "and ub:", ub)
        # generate MiniZinc data file
        data_file = "data.dzn"
        generateMinizincDataFile(node_count, edge_count, ub, ub, edges, data_file)

        # solve with Minizinc's MIP solver (CBC of COIN-OR)
        minizinc_proc = Popen(['minizinc', '-m', 'graphColoring.mzn', '-d', 'data.dzn'],
                stdout=PIPE, stderr=PIPE)
        try:
            (stdout, stderr) = minizinc_proc.communicate(timeout=timeout)
        except TimeoutExpired as exc:
            minizinc_proc.kill()
            minizinc_state = 'timeout'
        # any other exception
        except Exception as e:
            minizinc_proc.kill()
            minizinc_state = 'exception'
        else:
            # solution found
            if DEBUG:
                print ("solution found")
                print (stdout)
                print (stderr)
            satisfied = str(stdout, 'utf-8')
            lines = satisfied.split('\n')
            # check if it ended because it found a solution or if it's not satisfiable
            if 'UNSATISFIABLE' in lines[0]:
                minizinc_state = 'nsat'
            else:
                minizinc_state = 'sat'

        if minizinc_state == 'timeout':
            # the problem is too big for this timeout
            if DEBUG:
                print ("It wasnt possible to execute with the timeout,", timeout)
            break
        elif minizinc_state == 'exception':
            if DEBUG:
                print ("Unknown error occured")
            break
        elif minizinc_state == 'nsat':
            # ok, now we reached the limit considering the current timeout
            break
        else:
            # solution found !
            if best_ub > ub:
                best_ub = ub
                colors, solution = extractSolution(stdout,node_count)
                #best_solution = (colors, solution)
                # let's repeat with a tigher upper bound and see if it's still satisfiable within the timeout
                ub -= 1

    output_data = None
    # if the last execution was unsatiafiable but a solution was found in the previous iterations, then an optimal solution was found
    if len(solution) > 0 and minizinc_state=='nsat':
        optimal=1
    else:
        optimal=0
    if len(solution) > 0:
        if DEBUG:
            if G.number_of_edges() <= 300:
                # generate the colored graph
                graph_dot(G, max_clique, int(colors), solution)
            else:
                print ("the graph is too big to plot")

        # prepare the solution in the specified output format
        output_data = str(colors) + ' ' + str(optimal) + '\n'
        output_data += ' '.join(map(str, solution))
    else:
        print ("Aborted!")

    return output_data

###################################################################################
def nxGraph(edges):
    """ It generates a Networkx graph.
    """
    G = nx.Graph()

    for e in edges:
        G.add_edge(e[0], e[1])
    
    # The core of graph G is the subgraph of G obtained by the
    #   iterated removal of all vertices of degree 1 from G 
    # from: Classical Coloring of Graphs
    # Remove all nodes with degree 1
    original_num_nodes = G.number_of_nodes()
    if DEBUG:
        print ('%d nodes and %d edges before prunning nodes with degree 1' % (G.number_of_nodes(), G.number_of_edges()))
    # althouth it makes sense to prune these nodes for ordinary graphs.
    # it complicates the end of the algorithm and it does not provide improvements for the 
    # most complex coursera dataset, which has high degree
    #G = nx.k_core(G,k=2)
    if DEBUG:
        print ('%d nodes and %d edges after prunning' % (G.number_of_nodes(), G.number_of_edges()))

    # The number g(G) = 2m/(n(n − 1)) is known as the density of graph G.    
    m = G.number_of_nodes()
    n = G.number_of_edges()
    if DEBUG:
        print ('Graph density:', 2*m/(n*(n - 1)))

    return original_num_nodes, G

###################################################################################
def upper_bound(G):
    # run heuristics as a upper bound
    strategies = ['largest_first', 'random_sequential', 'smallest_last', 'independent_set',
        'connected_sequential_bfs', 'connected_sequential_dfs', 'saturation_largest_first']
    # set of colors found by each execution
    colors = []
    heuristic_solutions = []

    for s in strategies:
        # reapet each strategy 3 times
        for i in range(3):
            d = nx.coloring.greedy_color(G,s)
            MaxKey = max(d, key=d.get)
            # if DEBUG:
            #     print (d[MaxKey]+1)
            #     print (d)
            colors.append(d[MaxKey]+1)
            #print (d)
            heuristic_solutions.append(d)

    # check the heuristics solutions to see if they are indeed valid ones. minizinc will be used to check the solution.
    # sort the solutions by the descending order of number of colors
    heuristic_solutions.sort(key=lambda item: item[max(item, key=item.get)], reverse=True)
    if DEBUG:
        print ('\n\n\nheuristic solutions:\n\n\n')
    skip_solutions_of_colors = 99999
    best_heuristic_solution = 99999
    for c in heuristic_solutions:
        num_colors = c[max(c, key=c.get)]+1
        # sort the solution by the color number
        sorted_tuples = sorted(c.items(), key=lambda item: item[1])
        sorted_dict = {k: v for k, v in sorted_tuples}        
        #print (c[max(c, key=c.get)]+1,'---', c)
        if num_colors >= skip_solutions_of_colors:
            continue

        # build the constraint text
        lines = []
        for k,v in sorted_dict.items():
            lines.append('constraint colors[%d] = %d;' % (k,v+1))
        lines.append('% number of colors:' + str(num_colors))
        # insert these new lines into the minizinc model template
        gen_model(G, lines, 'satisfy-template.mzn', 'check_heur.mzn')
        # run minizinc to test the solution
        minizinc_proc = Popen(['minizinc', '-m', 'check_heur.mzn', '-d', 'data.dzn'],
                stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = minizinc_proc.communicate()

        # If minizinc tells that the heuristic solution is unfeasible, then go to the next one
        # since it's no use to test other solution with the same number of colors.
        # Else, if the solution is feasible, jump to another solution with fewer colors. 
        # Stop when all solutions were tested and we got at least on feasible solution, hopefully 
        # with the minimal number of colors to give a tigher bound.

        # check if it ended because it found a solution or if it's not satisfiable
        stdout = str(stdout, 'utf-8')
        stdout = stdout.split('\n')
        if 'UNSATISFIABLE' in stdout[0]:
            # try the next one
            if DEBUG:
                print ('bad heuristic solution of size', num_colors, c)
            pass
        else:
            # try the next one with fewer colors
            if DEBUG:
                print ('good heuristic solution of size', num_colors, c)
            skip_solutions_of_colors = num_colors
            best_heuristic_solution = num_colors
        

    # According to the book: "A Guide to Graph Colouring: Algorithms and Applications", 
    #  Section '2.2.2 Upper bounds',  the max degree can be used as an upper bound
    # In addition, heuristics are run to try to get a better upper bound
    degrees = []
    if DEBUG:
        print ('nodes with low degree:')
    low_deg_cnt = 0
    for node in range(G.number_of_nodes()):
        if DEBUG:
            if G.degree(node) <= 2:
                print (node)
                low_deg_cnt +=1
        degrees.append(G.degree(node)+1)
    max_degree = max(degrees)
    min_degree = min(degrees)
    avg_degree = statistics.mean(degrees)
    med_degree = statistics.median(degrees)

    if DEBUG:
        print ('heur upper bound:', colors)
        print ('stats (max, min, avg, med, low_deg_cnt):', max_degree, min_degree, avg_degree, med_degree, low_deg_cnt)
        #res_list = [i for i, value in enumerate(degrees) if value == 0] 
        #print (res_list)


    return max_degree, best_heuristic_solution

###################################################################################
def check_clique(G, clique):
    clique_set = set(clique)
    is_clique = True
    for node in clique:
        # remove the node form the clique
        neighbors = clique_set - {node}
        # if the set of adjacent nodes is a superset of neighbors, then it's ok, otherwise, is not a clique
        if not (set(G.adj[node]) >= neighbors):
            is_clique = False
    return is_clique

###################################################################################
def get_cliques(G):

    # searching the cliques in G
    cliques = []
    max_clique = clique.max_clique(G)
    if not check_clique(G,max_clique):
        # crappy heuristics returned a false clique. ignore it
        max_clique = []
    # not recommended for graphs with more than 250 nodes. it has a huge memory use !
    if G.number_of_nodes() < 250:
        cliques = list(nx.algorithms.clique.find_cliques(G))
    #print (type(cliques[0]))

    # sort the cliques by descending number of items.
    sorted_cliques = []
    for i in cliques:
        if len(i) >= 3:
            sorted_cliques.append((i,len(i)))
    sorted_cliques.sort(key=lambda a: a[1],reverse=True)
    # sometimes, the clique.max_clique does not deliver the actual max
    # get the next better and actual clique
    for i in range(len(sorted_cliques)):
        if sorted_cliques[i][1] > len(max_clique):
            max_clique = sorted_cliques[0][0]
            # if this clique is good, then use it as max_clique, else, accept the next good clique as max_clique
            if check_clique(G,max_clique):
                break
    # remove the tuple to become a list of sets representing the cliques
    sorted_cliques = [a[0] for a in sorted_cliques]
    if DEBUG:
        print ('max clique:', len(max_clique), max_clique)
        print ('n cliques:', len(sorted_cliques))
        # for i in sorted_cliques:
        #     print (i)

    return max_clique, sorted_cliques

###################################################################################
def gen_model(G, new_model_lines, templace_filename, model_filename):

    # reading the minizinc template to insert the clique constraints
    mzn_tpl_file = open(templace_filename, 'r')
    mzn_data = ''.join(mzn_tpl_file.readlines())
    mzn_tpl_file.close()
    lines = mzn_data.split('\n')

    # find the place to insert the custom constraints
    i = 0
    line_pos = 0
    for l in lines:
        if 'PUT_CLIQUES_HERE' in l:
            del(lines[i])
            line_pos = i
            break
        i +=1

    # insert the new lines to the model
    for l in new_model_lines:
        lines.insert(line_pos,l)

    # sort the nodes in ascending order of degree
    degree_list = []
    for n in G.nodes():
        degree_list.append((n,len(G.adj[n])))
    degree_list.sort(key=lambda a: a[1])

    #for i in degree_list:
    #    print (i)

    # A vertex u is dominated by a vertex v, v =
    # u, if the neighborhood of u is a subset of the
    # neighborhood of v. In this case, the vertex u can be deleted from G, the remaining graph
    # can be colored, and at the end, u can get the same color as v.
    
    # this idea comes form the paper "New Integer Linear Programming Models for the Vertex Coloring Problem"
    # unfortunatly, coursera's dataset do not have this situation, so it's useless
    #print ('NODE DOMINANCE')
    # for n in degree_list:
    #     if n[1] < len(max_clique):
    #         neighbors = set(G.adj[n[0]])
    #         inter = neighbors.intersection(max_clique)
    #         diff = list(neighbors.difference(inter))
    #         # the node n is dominated by max_clique
    #         if len(diff) == 0:
    #             diff = list(max_clique.difference(neighbors))
    #             lines.insert(line_pos,'constraint colors[%d] == %d;' % (n, color_codes[diff[0]]))
    #     else:
    #         break



    # # check if there is only one difference among the cliques to increase the # of defined nodes
    # for c1 in sorted_cliques:
    #     if len(c1) == len(max_clique):
    #         set1 = set(c1)
    #         inter = set1.intersection(max_clique)
    #         diff1 = list(set1.difference(inter))
    #         diff2 = list(max_clique.difference(inter))
    #         if len(diff1) == 1 and len(diff2) == 1:
    #             # print ("DIFF")
    #             # print (max_clique,c1)
    #             # print (inter, diff1, diff2)
    #             lines.insert(line_pos,'constraint colors[%d] == colors[%d];' % (diff1[0], diff2[0]))

    # # check if there is only one difference among the cliques to increase the # of defined nodes
    # no_adj_clique = []
    # for c1 in range(len(sorted_cliques)-1):
    #     for c2 in range(c1+1,len(sorted_cliques)):
    #         if len(sorted_cliques[c1]) == len(max_clique) and len(sorted_cliques[c2]) == len(max_clique):
    #             set1 = set(sorted_cliques[c1])
    #             set2 = set(sorted_cliques[c2])
    #             inter = set1.intersection(set2)
    #             diff1 = list(set1.difference(inter))
    #             diff2 = list(set2.difference(inter))
    #             if len(diff1) == 1 and len(diff2) == 1:
    #                 print ("DIFF")
    #                 print (sorted_cliques[c1],sorted_cliques[c2])
    #                 print (inter, diff1, diff2)
    #                 lines.insert(line_pos,'constraint colors[%d] == colors[%d];' % (diff1[0], diff2[0]))

    # # check if the cliques are adjacents
    # # check if any node of clique1 is connected to any node of clique2
    # no_adj_clique = []
    # for c1 in range(len(sorted_cliques)-1):
    #     for c2 in range(c1+1,len(sorted_cliques)):
    #         adj = False
    #         for c1i in sorted_cliques[c1]:
    #             for c2i in sorted_cliques[c2]:
    #                 if G.has_edge(c1i,c2i):
    #                     adj = True
    #                     break
    #             if adj:
    #                 break
    #         if not adj:
    #             print ("not adjacents:")
    #             print (sorted_cliques[c1])
    #             print (sorted_cliques[c2])
    #             no_adj_clique.append((sorted_cliques[c1],sorted_cliques[c2]))

    # print ("NOT ADJCENT CLIQUES:", len(no_adj_clique))
    # for i in no_adj_clique:
    #     print (i[0], i[1])


    # # for all the rest of the cliques, assign alldifferent
    # list_good_cliques = []
    # list_good_cliques.append(max_clique)
    # set_all_cliques = set()
    # for c in cliques:
    #     #print (c)
    #     c = set(c)
    #     # skip the smaller cliques to avoid too many constraints
    #     good_clique_sizes = range(len(max_clique)-3,len(max_clique)+1)
    #     if len(c) in good_clique_sizes:
    #         z = {}
    #         for g in list_good_cliques:
    #             z = g.intersection(c)
    #             if len(z) != 0:
    #                 break
    #         if len(z) == 0:
    #             print ('good clique:', c)
    #             list_good_cliques.append(c)
    #             set_all_cliques = set_all_cliques.union(c)
    #             # j=0
    #             # for n in c:
    #             #     lines.insert(line_pos,'constraint colors[%d] = %d;' % (n,j+1))
    #             #     j +=1                
    #             # alldiff='['
    #             # j=0
    #             # for n in c:
    #             #     alldiff +='colors['+str(n)+']'
    #             #     if j < len(c)-1:
    #             #         alldiff +=','
    #             #     j +=1
    #             # alldiff +=']'
    #             # lines.insert(line_pos,'constraint alldifferent(%s);' % alldiff)

    # print ('\n\\n\n GOOD CLIQUES:', len(list_good_cliques))
    # print ('set_all_cliques:', len(set_all_cliques))
    # print (set_all_cliques)
    # # transfor the set into list
    # set_all_cliques = list(set_all_cliques)
    # cliques_dict = dict()
    # for i in range(len(set_all_cliques)):
    #     cliques_dict[set_all_cliques[i]] = 0
    # for i in range(len(set_all_cliques)-1):
    #     for j in range(i+1, len(set_all_cliques)):
    #         if G.has_edge(set_all_cliques[i],set_all_cliques[j]):
    #             cliques_dict[set_all_cliques[i]] += 1
    #             cliques_dict[set_all_cliques[j]] += 1
    
    # print ('DICTIONARY:')
    # for key in cliques_dict:
    #     print (key, cliques_dict[key])

    # for i in list_good_cliques:
    #     print (i)

    # # check if the cliques are adjacents
    # # check if any node of clique1 is connected to any node of clique2
    # no_adj_clique = []
    # for c1 in range(len(list_good_cliques)-1):
    #     for c2 in range(c1+1,len(list_good_cliques)):
    #         adj = False
    #         for c1i in list_good_cliques[c1]:
    #             for c2i in list_good_cliques[c2]:
    #                 if G.has_edge(c1i,c2i):
    #                     adj = True
    #                     break
    #             if adj:
    #                 break
    #         if not adj:
    #             print ("not adjacents:")
    #             print (list_good_cliques[c1])
    #             print (list_good_cliques[c2])
    #             no_adj_clique.append((list_good_cliques[c1],list_good_cliques[c2]))

    # print ("NOT ADJCENT CLIQUES:", len(no_adj_clique))
    # for i in no_adj_clique:
    #     print (i[0], i[1])


    # create the minizinc model with the alldifferent constraints
    mzn_tpl_file = open(model_filename, 'w')
    for item in lines:
        mzn_tpl_file.write("%s\n" % item)
    mzn_tpl_file.close()


###################################################################################
def gen_model2(G):

    # reading the minizinc template to insert the clique constraints
    mzn_tpl_file = open('graphColoring-template.mzn', 'r')
    mzn_data = ''.join(mzn_tpl_file.readlines())
    mzn_tpl_file.close()
    lines = mzn_data.split('\n')

    # searching the cliques in G
    max_clique = [1]
    if G.number_of_nodes() <= 500:
        # not recommended for graphs with more than 500 nodes
        max_clique = clique.max_clique(G)

    # create the minizinc model with the alldifferent constraints
    mzn_tpl_file = open('graphColoring.mzn', 'w')
    for item in lines:
        mzn_tpl_file.write("%s\n" % item)
    mzn_tpl_file.close()

###################################################################################
def gen_model3(G):

    # reading the minizinc template to insert the clique constraints
    mzn_tpl_file = open('graphColoring-template.mzn', 'r')
    mzn_data = ''.join(mzn_tpl_file.readlines())
    mzn_tpl_file.close()
    lines = mzn_data.split('\n')

    # searching the cliques in G
    max_clique = [1]
    if G.number_of_nodes() <= 500:
        # not recommended for graphs with more than 500 nodes
        max_clique = clique.max_clique(G)
        #print (max_clique)

    i = 0
    line_pos = 0
    for l in lines:
        if 'PUT_CLIQUES_HERE' in l:
            del(lines[i])
            line_pos = i
            break
        i +=1

    # alldiff='['
    # j=0
    # for n in max_clique:
    #     alldiff +='colors['+str(n)+']'
    #     if j < len(max_clique)-1:
    #         alldiff +=','
    #     j +=1
    # alldiff +=']'
    # lines.insert(line_pos,'constraint alldifferent(%s);' % alldiff)

    j=0
    for n in max_clique:
        lines.insert(line_pos,'constraint colors[%d] = %d;' % (n,j+1))
        j +=1


    # create the minizinc model with the alldifferent constraints
    mzn_tpl_file = open('graphColoring.mzn', 'w')
    for item in lines:
        mzn_tpl_file.write("%s\n" % item)
    mzn_tpl_file.close()


###################################################################################
def graph_dot(G, max_clique, colors, solution, filename='graph'):
    """ It generates graphviz graphs.
    """

    if DEBUG:
        print ('writing the graph ...')
    # open the color file
    color_file = open('svg_colors', 'r')
    color_data = ''.join(color_file.readlines())
    color_file.close()
    lines = color_data.split('\n')
    # remove the trailing white spaces
    lines = [ele.replace(' ', '') for ele in lines]
    lines = [ele.replace('\t', '') for ele in lines]

    selected_colors = []
    # randomly select a set of colors
    i = colors
    while i>0:
        new_color = lines[random.randint(0, len(lines)-1)]
        if new_color not in selected_colors:
            selected_colors.append(new_color)
            i -=1

    if DEBUG:
        print ('selected colors:', selected_colors)
        print ('solution:', solution)

    # transforms NetworkX into PyG AGraph
    A = nx.nx_agraph.to_agraph(G)

    # the nodes in the max clique have a different shape
    for i in range(len(solution)):
        n=A.get_node(i)
        color_code = solution[i]-1
        n.attr['fillcolor'] = selected_colors[color_code]
        n.attr['style']='filled'
        node_id = int(n.get_name())
        if node_id in max_clique:
            n.attr['shape']= 'doubleoctagon'
            # add a fat line for the edges of the max clique
            for c in max_clique:
                if c != node_id:
                    edge=A.get_edge(n.get_name(),str(c))
                    edge.attr['penwidth'] = 4.0

    # create the legend
    # legend_nodes = []
    # for i in range(len(selected_colors)):
    #     node_name = 'c'+str(i)
    #     A.add_node(node_name)
    #     n=A.get_node(node_name)
    #     n.attr['fillcolor'] = selected_colors[i]
    #     legend_nodes.append(node_name)
    #     n.attr['style']='filled'
    # A.add_subgraph(name='cluster1', nbunch= legend_nodes, label='legend', color = 'black', rank='same')

    # simpler legend
    A.graph_attr['label'] = 'Number of colors %d' % (colors)
    A.graph_attr['labelloc'] = 't'
    A.graph_attr['labelfontsize'] = 1.4 * G.number_of_nodes() - 15
    
    A.write(filename+".dot")
    # change here the plot layout
    A.layout(prog='circo')
    A.draw(filename+".png")


###################################################################################
# not working. it misses some form of auto color assignment
def graph_pyplot(G, colors, solution):

    for n in G.nodes():
        color_code = solution[n]-1
        G.nodes[n]['color'] = selected_colors[color_code]

    nx.draw(G, with_labels = True) 
    plt.savefig("graph.svg") 

###################################################################################
def generateMinizincDataFile(node_count, edge_count, lb, ub, edges, data_file):
    tmpFile = open(data_file, 'w')
    
    out = "% automatically generated Minizinc data file\n"
    out += "ubc = " + str(ub)+ ";\n"
    out += "lbc = " + str(lb)+ ";\n"
    out += "nbNodes = " + str(node_count)+ ";\n"
    out += "nbEdges = " + str(edge_count)+ ";\n"
    out += "edges1 = [ " 
    cnt = 0
    for s in edges: 
        out += str(int(s[0]))
        if cnt == len(edges)-1:
            out += "];\n"
        else: 
            out += ", "
        cnt += 1
    out += "edges2 = [ " 
    cnt = 0
    for s in edges: 
        out += str(int(s[1]))
        if cnt == len(edges)-1:
            out += "];\n"
        else: 
            out += ", "
        cnt += 1

    tmpFile.write(out)
    tmpFile.close()
###################################################################################
def extractSolution(stdout,node_count):
    solution = [0]*node_count
    
    stdout = str(stdout, 'utf-8')
    lines = stdout.split('\n')   
    nColors = lines[0]
    line = lines[1]
    # the second line is expected in this format
    # [1, 0, 1, 1]
    # remove the 1st and the last char
    line = line[1:-1]
    words = line.split(', ')
    if len(words) != node_count:
        print ("Error in number of solutions")
    else:
        for i in range(0,len(words)):
            solution[i] = int(words[i])

    return nColors, solution

###################################################################################
# See 'Matrix Reordering Methods for Table and Network Visualization'
# to understand the seriation problem
# See https://github.com/amamory/seriation for the seriation program
def seriate(filename):
    # coursera datafile
    coursera_file = open(filename, 'r')
    graph_data = ''.join(coursera_file.readlines())
    coursera_file.close()
    lines = graph_data.split('\n')
    # the 1st line of coursera file is not used by seriation
    del(lines[0])
    # empty lines must be deleted
    lines = [i for i in lines if i] 


    # building the original graph
    oG = nx.OrderedGraph()
    for i in range(len(lines)):
        parts = lines[i].split()
        if len(parts) == 2:
            oG.add_edge(int(parts[0]), int(parts[1]))
    print ("original graph:")
    print (oG.number_of_nodes())
    print (oG.number_of_edges())

    # plot the not seriated matrix
    m = MatrixPlot(oG)
    m.draw()
    plt.savefig("nseriated.png") 

    # just have to remove the 1st line 
    seriation_ifile = open('graph.dat', 'w')
    for item in lines:
        seriation_ifile.write("%s\n" % item)
    seriation_ifile.close()

    # run seriation
    run_seriation('graph.dat')

    # read the seriated graph
    seriation_ofile = open('seriated.dat', 'r')
    graph_data = ''.join(seriation_ofile.readlines())
    seriation_ofile.close()
    lines = graph_data.split('\n')
    # empty lines must be deleted
    lines = [i for i in lines if i] 

    # making is a list of tuple to perform sort
    sorted_nodes = []
    for l in lines:
        parts = l.split()
        sorted_nodes.append((int(parts[0]),int(parts[1])))
    sorted_nodes.sort(key=lambda a: a[1])

    # save back the ordered seriation file
    seriation_ofile = open('seriated.dat', 'w')
    for item in sorted_nodes:
        seriation_ofile.write("%d %d\n" % (item[0], item[1]))
    seriation_ofile.close()
    # print ("sorted nodes")
    # for i in sorted_nodes:
    #     print (i)

    # building the graph
    seriation_ofile = open('seriated_graph.dat', 'w')
    G = nx.OrderedGraph()
    for i in sorted_nodes:
        node_id = i[0]
        for n in oG.adj[node_id]:
            G.add_edge(node_id, n)
            seriation_ofile.write("%d %d\n" % (node_id, n))
    seriation_ofile.close()
        
    # uncheck it to see if the graphs are still the same    
    #graph_dot(G, 1, [1]*G.number_of_nodes(),'seriated_graph')
    if not nx.is_isomorphic(oG, G):
        print ("ERROR: both graphs are not isomorphic")
    else:
        print ("both graphs are isomorphic")

    print ("seriated graph:")
    print ([i[0] for i in sorted_nodes])
    print (G.number_of_nodes())
    print (G.number_of_edges())

    # plot the seriated matrix
    m = MatrixPlot(G)
    m.draw()
    plt.savefig("seriated.png") 

    
###################################################################################
def run_seriation(graph_filename):

    graph_filename = 'f='+graph_filename
    proc = Popen(['./cfm-seriation', graph_filename],
            stdout=PIPE, stderr=PIPE)
    try:
        proc.communicate()
    except Exception as e:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM) 
        proc.kill()
        print ("Error running seriation")
        sys.exit(1)
        

# ##################################################################################        
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        # if DEBUG:
        #     seriate(file_location)
        print ('Solving:', file_location)
        print (solve_it(input_data))
    else:
        print ('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/sc_6_1)')
