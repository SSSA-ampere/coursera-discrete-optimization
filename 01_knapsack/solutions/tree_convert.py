#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import networkx as nx
import os, sys

if __name__ == '__main__':
    if len(sys.argv) > 3:
        if not os.path.isfile(sys.argv[1]):
            print ("ERROR: file", sys.argv[1], "not found")
            sys.exit(1)

        G = nx.read_gpickle(sys.argv[1])
        print ("converting a tree of", G.number_of_nodes(), "nodes ...")
        if G.number_of_nodes() > 1000:
            print ("WARNING: the tree is very big. You will probably run out of memory!")
            input("Press any to continue or CTRL+C to abort...")
        if sys.argv[2] == 'dot':
            nx.drawing.nx_pydot.write_dot(G, sys.argv[3])
        elif sys.argv[2] == 'adjlist':
            nx.write_adjlist(G, sys.argv[3])
        elif sys.argv[2] == 'yaml':
            nx.write_yaml(G, sys.argv[3])
        elif sys.argv[2] == 'edgelist':
            nx.write_edgelist(G, sys.argv[3], data=True)
        else:
            print ("ERROR: unsupported output format", sys.argv[2])
    else:
        print("ERROR: The required arguments are:")
        print (" $ ./tree_convert <input_pickle_file> <output_format> <ouput_filename>')")
        print (" suported formats: dot, adjlist, edgelist, yaml")
