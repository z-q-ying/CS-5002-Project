import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_node('A')
G.add_node('B')
G.add_node('C')
G.add_node('D')
G.add_node('E')
G.add_node('F')
G.add_node('G')
G.add_node('H')

G.add_edge('A', 'D')
G.add_edge('B', 'C')
G.add_edge('C', 'D')
G.add_edge('C', 'F')
G.add_edge('E', 'F')
G.add_edge('A', 'B')
G.add_edge('E', 'G')
G.add_edge('E', 'G')
G.add_edge('G', 'H')
G.add_edge('D', 'H')

V = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 2, 'F': 4, 'G': 3, 'H': 2}

for i, j in G.edges():
    G[i][j]['weight'] = V[str(i)] + V[str(j)]

nx.get_edge_attributes(G, 'weight')


def show_graph():
    nx.draw(G, with_labels=True, font_color='white', node_shape='s')


def show_wgraph():
    plt.figure()
    pos = nx.spring_layout(G)
    weight_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, font_color='white', node_shape='s', with_labels=True,)
    output = nx.draw_networkx_edge_labels(G, pos, edge_labels=weight_labels)


def show_wpath(from_node, to_node):
    plt.figure()
    pos = nx.spring_layout(G)

    weight_labels = nx.get_edge_attributes(G, 'weight')

    path = nx.shortest_path(G, source=from_node, target=to_node)

    edges_path = list(zip(path, path[1:]))
    edges_path_reversed = [(y, x) for (x, y) in edges_path]
    edges_path = edges_path + edges_path_reversed
    edge_colors = [
        'black' if not edge in edges_path else 'red' for edge in G.edges()]

    nodecol = ['steelblue' if not node in path else 'red' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, font_color='white',
            edge_color=edge_colors, node_shape='s', node_color=nodecol)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weight_labels)


# show_wgraph()
show_wpath('A', 'G')

plt.show()
