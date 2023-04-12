# Notebook 2.2- Weighted and directed graphs
# https://transport-systems.imperial.ac.uk/tf/60008_21/n2_2_weighted_and_directed_graphs.html

import networkx as nx
import matplotlib.pyplot as plt

#################################
# Part 1 - Function Definitions #
#################################

G = nx.Graph()


def show_graph(graph=G):
    nx.draw(graph, with_labels=True, font_color='white', node_shape='s')


def save_graph(filename):
    filename = filename + '.png'
    plt.savefig(filename, format="PNG")


G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)

G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(2, 4)

show_graph()  # nx.draw(G, with_labels=True, font_color='white', node_shape='s')
save_graph('g3')  # plt.savefig("g3.png", format="PNG")
plt.clf()  # this is important to add, need to repaint the whole thing

G.add_edge(4, 5)
G.add_edge(3, 6)
G.add_edge(5, 7)
G.add_edge(6, 7)
G.add_edge(7, 8)
G.add_edge(2, 7)

show_graph()
save_graph('g4')
plt.clf()

path = nx.shortest_path(G, source=1, target=8)  # [1, 2, 7, 8]
edges_path = list(zip(path, path[1:]))  # [(1, 2), (2, 7), (7, 8)]

# Note that we have reused our edge reversion "hack" to overcome the issues that
# we encountered with bidirectionality, when it comes to highlighting the edges
# that are used by our path...
# For directed paths, we don't need to the reversed paths
edges_path_reversed = [(y, x) for (x, y) in edges_path]  # [(2, 1), (7, 2), (8, 7)]
edges_path = edges_path + edges_path_reversed  # [(1, 2), (2, 7), (7, 8), (2, 1), (7, 2), (8, 7)]

edge_colors = ['black' if edge not in edges_path else 'red' for edge in G.edges()]
print(edges_path)
print(G.edges())
print(edge_colors)
nx.draw(G, with_labels=True, font_color='white', edge_color=edge_colors, node_shape='s')
save_graph('g5')
plt.clf()

# The highlighted edges definitely look useful, but wouldn't it be nice
# if we also highlighted the nodes? We can do this using the node_color parameter
path = nx.shortest_path(G, source=1, target=8)
node_col = ['steelblue' if node not in path else 'red' for node in G.nodes()]
nx.draw(G, with_labels=True, font_color='white', edge_color=edge_colors, node_shape='s', node_color=node_col)
save_graph('g6')
plt.clf()


def show_path(from_node, to_node):
    path = nx.shortest_path(G, source=from_node, target=to_node)
    edges_path = list(zip(path, path[1:]))
    edges_path_reversed = [(y, x) for (x, y) in edges_path]
    edges_path = edges_path + edges_path_reversed
    edge_colors = ['black' if edge not in edges_path else 'red' for edge in G.edges()]
    nodecol = ['steelblue' if node not in path else 'red' for node in G.nodes()]
    nx.draw(G, with_labels=True, font_color='white', edge_color=edge_colors, node_shape='s', node_color=nodecol)
    save_graph('g7')
    plt.clf()


show_path(6, 4)

############################
# Part 2 - Weighted Graphs #
############################

# We have so far assumed that our graphs are weightless -
# when it comes to calculating shortest paths,
# networkx uses a default weight for each edge.
# We can inspect the parameter values using the following command
# We received a dictionary, with the edge values as a key and the weight as the value.
for i, j in G.edges():
    G[i][j]['weight'] = 1
G[2][7]['weight'] = 5
print(nx.get_edge_attributes(G, 'weight'))  # {(1, 2): 1, (2, 3): 1, ...}

# compute the positions of the nodes in the graph using the spring layout algorithm
# to make sure that the edge labels are rendered correctly,
# we need to fix position of the nodes. To do this, we use the nx.spring_layout() command,
# which automatically determines some positions for our graph -
# these are stored to the variable pos, and are then supplied to
# nx.draw() and nx.draw_networkx_edge_labels()
pos = nx.spring_layout(G)

# get the weight labels
weight_labels = nx.get_edge_attributes(G, 'weight')
nx.draw(G, pos, with_labels=True, font_color='white', edge_color=edge_colors, node_shape='s', node_color=node_col)
nx.draw_networkx_edge_labels(G, pos, edge_labels=weight_labels)
save_graph('g8')
plt.clf()


def show_wgraph():
    plt.figure()
    pos = nx.spring_layout(G)
    weight_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, font_color='white', node_shape='s', with_labels=True, )
    output = nx.draw_networkx_edge_labels(G, pos, edge_labels=weight_labels)


G[7][2]['weight'] = 9

show_wgraph()
save_graph('g9')
plt.clf()

def show_wpath(from_node, to_node):
    plt.figure()
    pos = nx.spring_layout(G)

    weight_labels = nx.get_edge_attributes(G, 'weight')

    # unless we explicitely tell it what weight values to consider,
    # it assumes that no weights should be used
    # dijkstra_path is a function in the NetworkX library that uses Dijkstra's algorithm
    # to find the shortest path in a weighted graph between two specified nodes,
    # given a source and target node. It returns a list of nodes representing the shortest path
    # from the source to the target node
    # path = nx.shortest_path(G, source=from_node, target=to_node)
    path = nx.dijkstra_path(G, source=from_node, target=to_node)

    edges_path = list(zip(path, path[1:]))
    edges_path_reversed = [(y, x) for (x, y) in edges_path]
    edges_path = edges_path + edges_path_reversed
    edge_colors = ['black' if edge not in edges_path else 'red' for edge in G.edges()]

    nodecol = ['steelblue' if node not in path else 'red' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, font_color='white', edge_color=edge_colors, node_shape='s', node_color=nodecol)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weight_labels)




show_wpath(1, 8)
save_graph('g10')
plt.clf()

############################
# Part 3 - Directed Graphs #
############################

G = nx.DiGraph()

G.add_node('Select')
G.add_node('B')
G.add_node('C')
G.add_node('D')
G.add_node('E')
G.add_node('F')

G.add_edge('Select', 'B', weight=3)
G.add_edge('Select', 'C', weight=2)
G.add_edge('B', 'C', weight=1)
G.add_edge('B', 'E', weight=3)
G.add_edge('C', 'D', weight=8)
G.add_edge('E', 'F', weight=4)
G.add_edge('D', 'F', weight=2)
G.add_edge('B', 'D', weight=4)
G.add_edge('E', 'D', weight=4)

show_wpath('Select', 'F')
save_graph('g12')
plt.clf()

