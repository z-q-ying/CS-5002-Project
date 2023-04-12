# Source: Building DAGs / Directed Acyclic Graphs with Python
# https://mungingdata.com/python/dag-directed-acyclic-graph-networkx/

import networkx as nx

"""Create a directed graph."""

graph1 = nx.DiGraph()  # DiGraph is short for “directed graph”
graph1.add_node(1)
graph1.add_node(2)
graph1.add_node(3)
graph1.add_edge(1, 2)
graph1.add_edge(2, 3)
print(graph1)

graph2 = nx.DiGraph()
graph2.add_edges_from([("root", "a"), ("a", "b"), ("a", "e"), ("b", "c"), ("b", "d"), ("d", "e")])
print(graph2)

graph3 = nx.DiGraph()
graph3.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])

"""Checking validity: if the DAG is valid"""

print(nx.is_directed(graph2))  # Output: True
print(nx.is_directed_acyclic_graph(graph2))  # Output: True

print(nx.is_directed(graph3))  # Output: True
print(nx.is_directed_acyclic_graph(graph3))  # Output: False

# TODO: Understand how this is implemented
# Directed graphs that aren’t acyclic can’t be topologically sorted i.e. a validity check must be performed first
print(list(nx.topological_sort(graph2)))  # Output: ['root', 'a', 'b', 'd', 'e', 'c']

"""Methods to get the shortest/longest path"""

print(nx.shortest_path(graph2, 'root', 'e'))  # Output: ['root', 'a', 'e']

print(nx.dag_longest_path(graph2))  # Output: ['root', 'a', 'b', 'd', 'e']

print(list(nx.topological_sort(graph2)))  # Output: ['root', 'a', 'b', 'd', 'e', 'c']

"""Multiple root: A directed graph can have multiple valid topological sorts.
m, n, o, p, q is another way to topologically sort this graph.
"""

graph = nx.DiGraph()
graph.add_edges_from([('m', 'p'), ('n', 'p'), ('o', 'p'), ('p', 'q')])
nx.is_directed(graph)  # => True
nx.is_directed_acyclic_graph(graph)  # => True
list(nx.topological_sort(graph))  # => ['o', 'n', 'm', 'p', 'q']

"""Draw the graph"""

from matplotlib import pyplot as plt

g1 = nx.DiGraph()
g1.add_edges_from([("root", "a"), ("a", "b"), ("a", "e"), ("b", "c"), ("b", "d"), ("d", "e")])
plt.tight_layout()
nx.draw_networkx(g1, arrows=True)
plt.savefig("g1.png", format="PNG")
plt.clf()  # a function in the matplotlib library of Python that clears the current figure

g2 = nx.DiGraph()
g2.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])
plt.tight_layout()
nx.draw_networkx(g2, arrows=True)
plt.savefig("g2.png", format="PNG")
plt.clf()
