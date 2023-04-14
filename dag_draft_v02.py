import networkx as nx
import matplotlib.pyplot as plt
import csv


######################
# Process input data #
######################

filename = "event_planning.csv"

# Define the virtual start and end nodes
start_node, end_node = 'VI', 'VO'

# Initialize a dictionary for nodes with virtual start and end nodes
id_duration_dict = {start_node: 0, end_node: 0}

# Initialize a dictionary for id-"id:duration" pair for matplotlib
id_to_name_dict = {start_node: start_node, end_node: end_node}

# Initialize an empty dictionary for id-description pair
id_description_dict = {}

# Initialize empty edge_list, each edge is to be stored as tuple
edge_list = []

# Read the CSV file, update node_dict, node_description_dict, and edge_list
with open(filename, 'r', encoding='UTF-8') as file:
    reader = csv.reader(file)
    next(reader)  # skip header row

    for row in reader:
        node_label = row[0]
        description = row[1]
        duration = int(row[2]) if row[2] else 0
        preceding = row[3].split(',') if row[3] else []
        
        # Add the node and its duration to id_to_name_dict
        id_to_name_dict[row[0]] = row[0]+':'+row[2]

        # Add the node and its duration to node_duration_dict
        id_duration_dict[id_to_name_dict[node_label]] = duration

        # Add the node and its description to node_description_dict
        id_description_dict[node_label] = description

        # If node has no preceding node, add edge from virtual start node
        if not preceding:
            edge = (id_to_name_dict[start_node], id_to_name_dict[node_label])
            if edge not in edge_list:
                edge_list.append(edge)
        else:
            # If node has preceding nodes, add edges accordingly
            for p in preceding:
                s = p.strip()
                edge = (id_to_name_dict[s], id_to_name_dict[node_label])
                if edge not in edge_list:
                    edge_list.append(edge)

# If node is not being pointed to, add edge to virtual end node
for node_label in id_duration_dict.keys():
    if node_label not in [e[0] for e in edge_list] and node_label != end_node:
        edge = (node_label, id_to_name_dict[end_node])
        if edge not in edge_list:
            edge_list.append(edge)


# Print user friendly message to inform the progress
print('\nDone with step 1: Process input data\n')
print('id_duration_dict:', id_duration_dict)
print('id_to_name_dict:', id_to_name_dict)
print('id_description_dict:', id_description_dict)
print('edge_list', edge_list)

######################################
# Represent the graph using networkx #
######################################

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

# Print user friendly message to inform the progress
print('\nDone with step 2: Represent the graph using networkx\n')
print(f'G is now a {G}')
print(f'G is a valid directed acyclic graph: {is_valid_DAG}')

##########################
# Find the critical path #
##########################

# Function to find the longest path (brute-force approach)
def find_longest_path(graph, start, end):
    longest_path = []
    longest_length = float('-inf')  # Initialize to negative infinity

    for path in nx.all_simple_paths(graph, start, end):
        # print(path)  # Test: 6 simple paths from VI to VO
        length = 0
        for node in path:
            length += id_duration_dict[node]
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
id_duration_dict.pop(start_node)
id_duration_dict.pop(end_node)
edge_list = [
    edge for edge in edge_list if start_node not in edge and end_node not in edge]

# Remove VI and VO from lists and dicts related to the critical path
longest_path.pop(0)
longest_path.pop(len(longest_path)-1)
edges_lp = [
    edge for edge in edges_lp if start_node not in edge and end_node not in edge]

# Update G.nodes() and G.edges() by removing VI, VO and their adjacent edges
G.remove_node(start_node)
G.remove_node(end_node)

# Print user friendly message to inform the progress
print('\nDone with step 3: Find the critical path\n')
print('The longest path is', longest_path, 'with a length of', longest_length)
print('The edges of the longest path is', edges_lp)

###################
# Format and plot #
###################

# Layout options: spring, spectral, planar, random, etc.
plt.figure()
pos = nx.shell_layout(G)
pos = {k: (v[0], -v[1]) for k, v in pos.items()}
node_col = ['red' if node in longest_path else 'steelblue' for node in G.nodes()]
edge_colors = ['red' if edge in edges_lp else 'grey' for edge in G.edges()]

# Draw DAG
nx.draw(G, pos, with_labels=True, font_color='white', edge_color=edge_colors,
        edgecolors='darkgray', node_color=node_col, node_size=700)

# If you want an image file as well as a user interface window,
# use pyplot.savefig before pyplot.show
# After show() the figure is closed and thus unregistered from pyplot
filename = filename + '.png'
plt.savefig(filename, format="PNG")
plt.show()
plt.clf()
