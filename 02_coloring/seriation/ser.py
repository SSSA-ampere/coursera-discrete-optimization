import os, sys, signal
from subprocess import Popen, check_output, PIPE, TimeoutExpired
import networkx as nx
from nxviz.plots import MatrixPlot
import matplotlib.pyplot as plt 


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
    print ("sorted nodes")
    for i in sorted_nodes:
        print (i)

    # building the graph
    G = nx.OrderedGraph()
    for i in sorted_nodes:
        node_id = i[0]
        for n in oG.adj[node_id]:
            print (node_id, n)
            G.add_edge(node_id, n)
        

    print ("seriated graph:")
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