import networkx as nx
import matplotlib.pyplot as plt
import csv

######################
# Process input data #
######################

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

######################
# Find Critical Path #
######################

# Global variables
# Create an empty directed graph Object
G = nx.DiGraph()
# Define the virtual start and end nodes
start_node = 'VI'
end_node = 'VO'

# Build the key-value dict
# Adding virtual-start node (VI stands for virtual-in)
# Rule: If a node N is not being pointed to, add (start_node, N)
node_dict = {start_node: 0, 'A': 3, 'B': 2, 'C': 2, 'D': 4,
             'E': 3, 'F': 2, 'G': 3, 'H': 1, 'I': 5,
             'J': 2, 'K': 10, end_node: 0}

# Build the edge lists
# Adding virtual-end node (VO stands for virtual-out)
# Rule: If a node N points to no node, add (N, end_node)
edge_list = [(start_node, 'A'), (start_node, 'B'), ('A', 'C'), ('B', 'C'),
             ('C', 'D'), ('C', 'E'), ('E', 'F'), ('D', 'F'),
             ('C', 'G'), ('G', 'H'), ('F', 'I'), ('H', 'J'),
             ('I', 'J'), ('J', 'K'), ('K', end_node)]

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
