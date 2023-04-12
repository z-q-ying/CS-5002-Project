import networkx as nx
import matplotlib.pyplot as plt
import csv

filename = "event_planning.csv"

# Initialize an empty dictionary to store the data
data = []

# Read the CSV file and store the data in the dictionary
with open(filename, newline='', encoding='UTF-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

# Print the data
# for item in data:
#     print(item)


# Global variable: Create an empty Weighted DAG (Directed Acyclic Graph)
G = nx.DiGraph()


# Function to find the longest path (brute-force approach)
def find_longest_path(graph, start, end):
    longest_path = []
    longest_length = float('-inf')

    for path in nx.all_simple_paths(graph, start, end):
        length = 0
        for i in range(len(path) - 1):
            length += graph.edges[path[i], path[i + 1]]['weight']
        if length > longest_length:
            longest_length = length
            longest_path = path

    return longest_path, longest_length


def save_graph(filename):
    filename = filename + '.png'
    plt.savefig(filename, format="PNG")


# Create the edges lists with labels and weights (can set a default weight)
edge_list_ww = [('A', 'B', 3), ('A', 'C', 2), ('B', 'C', 1), ('B', 'E', 3),
                ('C', 'D', 8), ('E', 'F', 4), ('D', 'F', 2),
                ('B', 'D', 4), ('E', 'D', 4)]

# Fill the Weighted DAG
G.add_weighted_edges_from(edge_list_ww)

# Graph validation: Returns True if the graph G is a DAG or False if not
print('is_directed_acyclic_graph: ', nx.is_directed_acyclic_graph(G))

# Define the start and end nodes
start_node = 'A'
end_node = 'F'

# Find the longest path given the start and end node
path, length = find_longest_path(G, start_node, end_node)
print(f"The longest path is {path} with a length of {length}")


# Formatting
edges_path = list(zip(path, path[1:]))
edge_colors = [
    'black' if edge not in edges_path else 'red' for edge in G.edges()]

pos = nx.spring_layout(G)
print('pos:', pos.items())  # dict_items([('A', array([-0.4,  0.76])), ...]

node_col = ['steelblue' if node not in path else 'red' for node in G.nodes()]

# Draw DAG (w/o weight labels)
nx.draw(G, pos, with_labels=True, font_color='white', edge_color=edge_colors,
        node_shape='s', node_color=node_col)


nx.draw(G, pos, with_labels=True, font_color='white',
        edge_color=edge_colors, node_shape='s')


# Draw the weight labels
weight_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=weight_labels)

# Plot the graph in various ways
# nx.draw_spring(G, with_labels=True)
# nx.draw_spectral(G, with_labels=True)
# nx.draw_planar(G, with_labels=True)
# nx.draw_random(G, with_labels=True)

# If you want an image file as well as a user interface window,
# use pyplot.savefig before pyplot.show
# After show() the figure is closed and thus unregistered from pyplot
save_graph('g14')
plt.show()
plt.clf()
