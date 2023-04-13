import networkx as nx
import matplotlib.pyplot as plt
import csv


######################
# Process input data #
######################

filename = "event_planning.csv"

# Define the virtual start and end nodes
start_node = 'VI'
end_node = 'VO'

# Initialize a dictionary for nodes with virtual start and end nodes
# TODO: rename to node_duration_dict
node_dict = {start_node: 0, end_node: 0}

# Initialize an empty dictionary for item-description pair
# To build the edge lists
node_description_dict = {}

# Initialize empty edge_list, each edge is stored as tuple
edge_list = []

# Read the CSV file, update node_dict, node_description_dict, and edge_list
with open(filename, 'r', encoding='UTF-8') as file:
    reader = csv.reader(file)
    next(reader)  # skip header row

    for row in reader:
        node = row[0]
        description = row[1]
        duration = int(row[2]) if row[2] else 0
        preceding = row[3].split(',') if row[3] else []

        # Add the node and its duration to node_duration_dict
        node_dict[node] = duration

        # Add the node and its description to node_description_dict
        node_description_dict[node] = description

        # If node has no preceding node, add edge from virtual start node
        if not preceding:
            edge = (start_node, node)
            if edge not in edge_list:
                edge_list.append(edge)
        else:
            # If node has preceding nodes, add edges accordingly
            for p in preceding:
                edge = (p.strip(), node)
                if edge not in edge_list:
                    edge_list.append(edge)

# If node is not being pointed to, add edge to virtual end node
for node in node_dict.keys():
    if node not in [e[0] for e in edge_list] and node != end_node:
        edge = (node, end_node)
        if edge not in edge_list:
            edge_list.append(edge)


######################
# Find Critical Path #
######################

# Global variables
# Create an empty directed graph Object
G = nx.DiGraph()

# Add edges to a graph from a list of edges
# The edges must be given as 2-tuples (u, v) or 3-tuples (u, v, d)
# where d is a dictionary containing edge data
G.add_edges_from(edge_list)

# Check if G is a valid Directed Acyclic Graph (DAG)
# Satisfy both conditions: Directed, Acyclic
is_valid_DAG = nx.is_directed_acyclic_graph(G)
print(f'G is a valid directed acyclic graph: {is_valid_DAG}')


# Function to find the longest path (brute-force approach)
def find_longest_path(graph, start, end):
    longest_path = []
    longest_length = float('-inf')  # Initialize to negative infinity

    for path in nx.all_simple_paths(graph, start, end):
        # print(path)  # Test: 6 simple paths from VI to VO
        length = 0
        for node in path:
            length += node_dict[node]
        if length > longest_length:
            longest_length = length
            longest_path = path

    return longest_path, longest_length


# TODO: Implement more efficient algorithm, and get bigO for the report
# Could compare run time etc.


# Find the longest path and its length
longest_path, longest_length = find_longest_path(G, start_node, end_node)
edges_lp = list(zip(longest_path, longest_path[1:]))

# Remove VI and VO from lists and dicts
# TODO: For the sake of good order only, may be deleted if not needed
node_dict.pop(start_node)
node_dict.pop(end_node)
edge_list = [edge for edge in edge_list if start_node not in edge and end_node not in edge]

# Remove VI and VO from lists and dicts related to the critical path
longest_path.pop(0)
longest_path.pop(len(longest_path)-1)
edges_lp = [edge for edge in edges_lp if start_node not in edge and end_node not in edge]

# Update G.nodes() and G.edges() by removing VI, VO and their adjacent edges
G.remove_node(start_node)
G.remove_node(end_node)

print('The longest path is', longest_path, 'with a length of', longest_length)
print('The edges of the longest path is', edges_lp)


###################
# Format and Plot #
###################

# TODO: Reformat the graph so that it looks like what's in the book

# Layout options: spring, spectral, planar, random, etc.
pos = nx.spring_layout(G)
node_col = ['red' if node in longest_path else 'steelblue' for node in G.nodes()]
edge_colors = ['red' if edge in edges_lp else 'grey' for edge in G.edges()]


# Draw DAG (w/o weight labels)
nx.draw(G, pos, with_labels=True, font_color='white', edge_color=edge_colors,
        node_color=node_col)


def save_graph(filename):
    """Helper function to save the graph"""
    filename = filename + '.png'
    plt.savefig(filename, format="PNG")


# If you want an image file as well as a user interface window,
# use pyplot.savefig before pyplot.show
# After show() the figure is closed and thus unregistered from pyplot
save_graph('g15')
plt.show()
plt.clf()
