import matplotlib.pyplot as plt
import networkx as nx
import os,sys
from networkx.drawing.nx_pydot import graphviz_layout
import plotly.graph_objs as go
import time

######################################
# tree ploting with graphviz
######################################
# 1) https://www.programcreek.com/python?code=isaacg1%2Fpyth%2Fpyth-master%2Ftree.py
# def disp_tree(trees):
#     graph = Digraph()
#     count = 0

#     def add(tree, count):
#         if not tree:
#             return count
#         root = count
#         graph.node(str(root), label=tree[0])
#         for subtree in tree[1:]:
#             if subtree:
#                 count += 1
#                 graph.edge(str(root), str(count))
#                 count = add(subtree, count)
#         return count
#     for tree in trees:
#         count = add(tree, count) + 1
#     graph.render('tree-rep.gv', view=True) 
####################################################
#
# 2) https://renenyffenegger.ch/notes/tools/Graphviz/examples/edge-crossing
#
# 3) https://anytree.readthedocs.io/en/latest/dotexport.html    <=======
#    https://stackoverflow.com/questions/57512155/how-to-draw-a-tree-more-beautifully-in-networkx
# 4) https://colab.research.google.com/drive/1Qq4TfF1XrsQZpNyOqjC4uL5saicPYOo1
#    https://github.com/uwdata/visualization-curriculum
#    https://altair-viz.github.io/gallery/#interactive-charts
#    https://nbviewer.jupyter.org/gist/msund/11349097


def plotly_tree(G, layout, title = '', edge_legend='', node_legend='', 
    edge_weight_attrib_name='weight', node_weight_attrib_name='weight',
    edge_hover_template='', node_hover_template='',
    edge_customdata=[], node_customdata=[]):
    """ Plot the graph using `Plotly <https://plotly.com/>`_.

    Args:
        G (:class:`networkx.DiGraph`): The directed graph.
        layout (str): One of the graph layouts supported by networkx.

    Returns:
        :class:`plotly.graph_objects.Figure`: The graph figure by plotly.


    """
    if layout == 'planar':
        pos = nx.planar_layout(G)
    elif layout == 'shell':
        pos = nx.layout.shell_layout(G)
    elif layout == 'spring':
        pos = nx.layout.spring_layout(G)
    elif layout == 'spectral':
        pos = nx.layout.spectral_layout(G)
    elif layout == 'spiral':
        pos = nx.layout.spiral_layout(G)
    elif layout == 'fruchterman_reingold':
        pos = nx.layout.fruchterman_reingold_layout(G)
    elif layout == 'dot':
        pos = nx.nx_pydot.pydot_layout(G, prog="dot")
    else:
        print ("ERROR: unsupported graph layout", layout)
        sys.exit(1)

    # insert the posistion property into the nodes
    for node in G.nodes:
        G.nodes[node]['pos'] = list(pos[node])

    # create the nodes
    traceRecode = []
    start_nodes = time.time()
    node_trace = go.Scatter(x=[], y=[], text=[], 
                            mode='markers+text', 
                            textposition="bottom center",
                            hoverinfo="text", 
                            marker=dict(
                                showscale=True,
                                # colorscale options
                                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                                #colorscale='Reds',
                                #reversescale=False,
                                color=[],
                                size=50,
                                # colorbar=dict(
                                #     thickness=15,
                                #     title=node_legend,
                                #     xanchor='left',
                                #     titleside='right'
                                # )
                            )
                        )
    end_nodes = time.time()

    # populating the nodes
    # zip split the tuple into 2 vectors
    x, y = zip(*list(nx.get_node_attributes(G,'pos').values()))
    node_trace['x'] = x
    node_trace['y'] = y
    node_trace['text'] = list(G.nodes())
    node_trace['hovertemplate'] = node_hover_template
    node_trace.marker.color = list(nx.get_node_attributes(G,'color').values())
    node_trace['customdata'] = node_customdata

    # creating the edges
    start_edges = time.time()
    for edge in G.edges:
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        #weight = float(G.edges[edge]['TransactionAmt']) / max(edge1['TransactionAmt']) * 10
        trace = go.Scatter(x=tuple([x0, x1, None]), y=tuple([y0, y1, None]),
                        mode='lines',
                        line=dict(width=0.5, color='#888'),
                        line_shape='spline'
                        #marker=dict(color=colors[index]),
                        #opacity=1
                        )
        # TODO add arrows 
        # https://plotly.com/python/text-and-annotations/
        #fig.add_annotation(x=x1, y=y1,
        #    showarrow=True,
        #    arrowhead=1)
        traceRecode.append(trace)
    end_edges = time.time()
    
    traceRecode.append(node_trace)

    start_fig = time.time()
    fig = go.Figure(
                #data=[edge_trace, middle_hover_trace, node_trace],
                data=traceRecode,
                layout=go.Layout(
                    title= title,
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    end_fig = time.time()

    return fig


def plotly(G, layout):
    """ plot an interactinve tree with Plotly.

    Args:
        G (:class:`networkx.DiGraph`): The directed graph.
        layout (str): One of the graph layouts supported by networkx.

    Returns:
        :class:`plotly.graph_objects.Figure`: The graph figure by plotly.

    """

    title = 'Knapsack Tree'
    edge_legend=''
    node_legend=''
    edge_weight_attrib_name='' 
    node_weight_attrib_name=''
    edge_hover_template="" 
    node_hovertemplate="<br>".join([
            "value: %{customdata[0]}",
            "estimate: %{customdata[1]}",
            "room: %{customdata[2]}"
        ])

    # populating the node hover data
    # the map converts every element of the list (int) into string
    # https://stackoverflow.com/questions/26320175/how-to-convert-integers-in-list-to-string-in-python#26320200
    value = list(map(str, list(nx.get_node_attributes(G,'value').values())))
    estimate = list(map(str, list(nx.get_node_attributes(G,'estimate').values())))
    room = list(map(str, list(nx.get_node_attributes(G,'room').values())))
    # convert the lists into a single list of 5-item tuple
    node_customdata = list(zip(value, estimate, room))
   
    # populating the edge hover data
    # since every edge is a new plotly scater, a list of customdata is necessary,
    # one for every edge of the graph
    edge_customdata = []
    #for edge in G.edges:
    #    edge_customdata.append((G.edges[edge]['name'], str(G.edges[edge]['size'])))

    fig = plotly_tree(G, layout, 
        title, edge_legend, node_legend, 
        edge_weight_attrib_name, node_weight_attrib_name, 
        edge_hover_template,node_hovertemplate, 
        edge_customdata, node_customdata
        )

    fig.show()


if __name__ == '__main__':
    if len(sys.argv) > 3:
        if not os.path.isfile(sys.argv[1]):
            print ("ERROR: file", sys.argv[1], "not found")
            sys.exit(1)

        G = nx.read_gpickle(sys.argv[1])
        pos = None
        print ("ploting a tree of", G.number_of_nodes(), "nodes ...")
        if sys.argv[2] == 'twopi':
            pos = graphviz_layout(G, prog="twopi")
        elif sys.argv[2] == 'dot':
            pos = graphviz_layout(G, prog="dot")
        elif sys.argv[2] == 'circo':
            pos = graphviz_layout(G, prog="circo")
        elif sys.argv[2] == 'plotly':
            plotly(G,'dot')
        elif sys.argv[2] == 'altair':
            print ("ERROR: not implemented yet")
            pass
        else:
            print ("ERROR: unsupported output format", sys.argv[2])


        if sys.argv[2] == 'twopi' or sys.argv[2] == 'dot' or sys.argv[2] == 'circo':
            node_colors = [v['color'] for n,v in G.nodes(data=True)]
            nx.draw(G, pos, node_color = node_colors)
            plt.show()
            p=nx.drawing.nx_pydot.to_pydot(G)
            p.write_png(sys.argv[3])

    else:
        print("ERROR: The required arguments are:")
        print (" $ ./tree_plot <input_pickle_file> <output_format> <ouput_filename>')")
        print (" suported formats: dot, twopi, circo, plotly, altair")

