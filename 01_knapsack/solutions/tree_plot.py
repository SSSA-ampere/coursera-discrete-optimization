import igraph as ig
import plotly.graph_objects as go 
#import random

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


def make_annotations(pos, labels, font_size=10, font_color='rgb(250,250,250)'):
    L=len(pos)
    if len(labels)!=L:
        raise ValueError('The lists pos and text must have the same len')
    annotations = []
    for k in range(L):
        annotations.append(
            dict(
                text=labels[k], # or replace labels with a different list for the text within the circle
                x=pos[k][0], y=2*M-position[k][1],
                xref='x1', yref='y1',
                font=dict(color=font_color, size=font_size),
                showarrow=False)
        )
    return annotations

def node_label(node_info):
    label =  "index=%d<br>value=%d<br>weight=%d" % (node_info[0],node_info[1],node_info[2])
    return label
   


def plot(plot_labels, edges):

    # to get max value in a list of tuples 
    max_node = max(map(max, zip(*edges)))
    graph = ig.Graph()
    graph.add_vertices(max_node+1)
    graph.add_edges(edges)
    #print(graph)
    #print(len(plot_labels), "----", plot_labels)
    #print(len(graph.vs), len(graph.es))

    for i in range(len(graph.vs)):
        graph.vs[i]["index"] = plot_labels[i][0]
        graph.vs[i]["value"] = plot_labels[i][1]
        graph.vs[i]["room"] = plot_labels[i][2]
        graph.vs[i]["estimate"] = plot_labels[i][3]

    #print(graph)

    fig = go.Figure()

    # https://igraph.org/python/doc/tutorial/tutorial.html#layouts-and-plotting
    lay = graph.layout('tree',root=[0])
    vnum = graph.vcount()
    position = {k: lay[k] for k in range(vnum)}
    Y = [lay[k][1] for k in range(vnum)]
    M = max(Y)

    #es = ig.EdgeSeq(graph)   # sequence of edges
    E = [e.tuple for e in graph.es]   # list of edges
    L = len(position)
    Xn = [position[k][0] for k in range(L)]     # x postion for vertices
    Yn = [2*M-position[k][1] for k in range(L)]  # y postion for vertices
    Xe = []
    Ye = []
    for edge in E:
        Xe += [position[edge[0]][0], position[edge[1]][0], None]
        Ye += [2*M-position[edge[0]][1], 2*M-position[edge[1]][1], None]

    # create just any random label 
    #node_tuple = (random.randint(0,10),random.randint(0,10),random.randint(0,10))
    #v_label = [node_label(node_tuple) for i in range(len(position))]
    #v_label = [i for i in range(len(position))]
    #print ("LEN:", len(v_label), len(position))

    #extracting vertixes info from 'plot_labels'
    indexes = []
    values = []
    rooms = []
    estimates = []
    hovertext = []
    for i in plot_labels:
        indexes.append(i[0])
        values.append(i[1])
        rooms.append(i[2])
        estimates.append(i[3])
        hovertext.append("Index:%d<br>Value:%d<br>Room:%d<br>Estimate:%.2f" % (i[0],i[1],i[2],i[3]))

    # add property for the vertixes. info not used for now
    graph.vs['index'] = indexes
    graph.vs['value'] = values
    graph.vs['room'] = rooms
    graph.vs['estimate'] = estimates

    # plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe, y=Ye, mode='lines',
                            line=dict(color='rgb(210, 210, 210)', width=1),
                            hoverinfo='none'))
    fig.add_trace(go.Scatter(x=Xn, y=Yn, name='bla',
                            mode='markers', 
                            marker=dict(symbol='circle-dot', 
                            size=18, color='#6175c1',
                            line=dict(color='rgb(50,50,50)', width=1)),
                            #text=graph.vs['name'],
                            hovertext=hovertext,
                            hoverinfo='text',
                            opacity=0.8))


    axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=True,
                showticklabels=True,
                )

    fig.update_layout(title= 'Knapsack Tree',
                #annotations=make_annotations(position, v_label),
                font_size=12,
                showlegend=False,
                xaxis=axis,
                yaxis=axis,
                margin=dict(l=40, r=40, b=85, t=100),
                hovermode='closest',
                plot_bgcolor='rgb(248,248,248)'
                )
    fig.show()

# enable this for testing
#edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
#plot_labels = [(0, 0, 31181, 12452.828296703297), (13, 3878, 21525, 12452.828296703297), (3, 8014, 11153, 12452.828296703297), (2, 10959, 3763, 12452.828296703297), (5, 11981, 1019, 12452.828296703297)]
#plot(plot_labels,edges)