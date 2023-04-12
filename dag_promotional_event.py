import networkx as nx
import matplotlib.pyplot as plt

# Global variable
G = nx.DiGraph()

def save_graph(filename):
    filename = filename + '.png'
    plt.savefig(filename, format="PNG")

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

if __name__ == '__main__':
    G.add_node('A')
    G.add_node('B')
    G.add_node('C')
    G.add_node('D')
    G.add_node('E')
    G.add_node('F')

    G.add_edge('A', 'B', weight=3)
    G.add_edge('A', 'C', weight=2)
    G.add_edge('B', 'C', weight=1)
    G.add_edge('B', 'E', weight=3)
    G.add_edge('C', 'D', weight=8)
    G.add_edge('E', 'F', weight=4)
    G.add_edge('D', 'F', weight=2)
    G.add_edge('B', 'D', weight=4)
    G.add_edge('E', 'D', weight=4)

    show_wpath('A', 'F')
    save_graph('g13')
    plt.clf()