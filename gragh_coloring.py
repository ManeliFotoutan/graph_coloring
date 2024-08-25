import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

# Set the backend to 'Agg' for non-interactive environments
matplotlib.use('Agg')

# Create a Graph
G = nx.Graph()

# Get the number of nodes and edges from the user
num_nodes = int(input("How many nodes? "))
num_edges = int(input("How many edges? "))

# Input nodes
for _ in range(num_nodes):
    node_input = input("Enter node (format 'node_id,label'): ")
    node_id, label = node_input.split(',')
    node_id = int(node_id)
    G.add_node(node_id, label=label)

# Input edges
for _ in range(num_edges):
    edge_input = input("Enter edge (format 'node1,node2'): ")
    node1, node2 = map(int, edge_input.split(','))
    # Skip self-loops
    if node1 != node2:
        G.add_edge(node1, node2)

# Define color constraints
k = int(input("Enter the number of colors: "))
color_limits = [int(input(f"Enter the maximum number of nodes for color {i+1}: ")) for i in range(k)]

# Map colors to a palette
color_map = matplotlib.colormaps.get_cmap('tab10')  # Get the colormap
colors = [color_map(i / (k - 1)) for i in range(k)]  # Generate a list of k colors

# Assign colors to nodes based on constraints
node_colors = {}
node_count = 0
for i, node in enumerate(G.nodes()):
    color_index = min(node_count // color_limits[i % k], k - 1)
    node_colors[node] = colors[color_index]
    node_count += 1

# Set node colors and edge attributes
nx.set_node_attributes(G, node_colors, 'color')
edge_thickness = {edge: 2 for edge in G.edges()}  # Default thickness
nx.set_edge_attributes(G, edge_thickness, 'thickness')

# Draw the Graph
pos = nx.spring_layout(G)  # Positions for all nodes

# Draw nodes
node_color_list = [G.nodes[node]['color'] for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_color_list)

# Draw edges
edge_thickness_list = [G.edges[edge]['thickness'] for edge in G.edges()]
nx.draw_networkx_edges(G, pos, width=edge_thickness_list)

# Draw labels
labels = nx.get_node_attributes(G, 'label')
nx.draw_networkx_labels(G, pos, labels, font_size=16)

# Save the plot to a file
plt.title("Graph with User Input")
plt.savefig('graph_plot.png')  # Save as PNG file
plt.close()  # Close the plot to free up resources
