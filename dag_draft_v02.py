import networkx as nx
import matplotlib.pyplot as plt
import csv


######################
# Process input data #
######################

# Read input data from CSV file and process it
filename = "event_planning.csv"

# Define virtual start and end nodes
start_node, end_node = 'VI', 'VO'

# # Initialize dictionaries and edge_list to store processed data
id_duration_dict = {start_node: 0, end_node: 0}
id_to_name_dict = {start_node: start_node, end_node: end_node}
id_description_dict = {}
edge_list = []

# Read and process CSV file
with open(filename, 'r', encoding='UTF-8') as file:
    reader = csv.reader(file)
    next(reader)  # skip header row

    for row in reader:
        # Process each row and update dictionaries and edge_list
        node_label = row[0]
        description = row[1]
        duration = int(row[2]) if row[2] else 0
        preceding = row[3].split(',') if row[3] else []
        
        # Deal with potential duplicate row inputs (as identified by id)
        if node_label in id_to_name_dict:
            continue

        # Add the node and its duration to id_to_name_dict
        id_to_name_dict[node_label] = node_label+':'+str(duration)

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


# Print processed input data
print('\nDone with step 1: Process input data')
print('id_duration_dict:', id_duration_dict)
print('id_to_name_dict:', id_to_name_dict)
print('id_description_dict:', id_description_dict)
print('edge_list', edge_list)

######################################
# Represent the graph using networkx #
######################################

# Create a directed graph object and add edges from the edge_list
G = nx.DiGraph()
G.add_edges_from(edge_list)

# Check if G is a valid Directed Acyclic Graph (DAG)
is_valid_DAG = nx.is_directed_acyclic_graph(G)

# Print graph representation information
print('\nDone with step 2: Represent the graph using networkx')
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


# Find the longest path and its length
longest_path, longest_length = find_longest_path(G, start_node, end_node)
edges_lp = list(zip(longest_path, longest_path[1:]))

# Update data structures by removing virtual nodes
id_duration_dict.pop(start_node)
id_duration_dict.pop(end_node)
edge_list = [edge for edge in edge_list if start_node not in edge and end_node not in edge]
longest_path.pop(0)
longest_path.pop(len(longest_path)-1)
edges_lp = [edge for edge in edges_lp if start_node not in edge and end_node not in edge]
G.remove_node(start_node)
G.remove_node(end_node)

# Print critical path information
print('\nDone with step 3: Find the critical path')
print('The longest path is', longest_path, 'with a length of', longest_length)
print('The edges of the longest path is', edges_lp)

###################
# Format and plot #
###################

# Set layout options and draw the graph using matplotlib
plt.figure()
pos = nx.shell_layout(G)
pos = {k: (v[0], -v[1]) for k, v in pos.items()}
node_col = ['red' if node in longest_path else 'steelblue' for node in G.nodes()]
edge_colors = ['red' if edge in edges_lp else 'grey' for edge in G.edges()]

# Draw DAG
nx.draw(G, pos, with_labels=True, font_color='white', edge_color=edge_colors,
        node_color=node_col, node_size=700)

# Save graph plot to file and display it
filename = filename + '.png'
plt.savefig(filename, format="PNG")
plt.show()
plt.clf()

# Print plot information
print('\nDone with step 4: Format and plot')
print(f'Picture is stored as {filename}')


###########################
# Generate output message #
###########################

# Function to generate and print a summary of the critical path
def generate_summary(longest_path, longest_length, id_description_dict):
    summary = "The critical path consists of the following tasks:\n"
    
    for idx, task in enumerate(longest_path):
        task_id = task.split(':')[0]
        task_description = id_description_dict[task_id]
        task_duration = task.split(':')[1]
        summary += f"{idx + 1}. {task_id}: {task_description} ({task_duration} days)\n"
    
    summary += f"\nThe total duration of the critical path is {longest_length} days."
    
    return summary

# Generate the summary and print it
print(f'\nSUMMARY\n')
summary = generate_summary(longest_path, longest_length, id_description_dict)
print(summary)
