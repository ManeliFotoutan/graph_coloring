import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

# Set the backend to 'Agg' for non-interactive environments
matplotlib.use('Agg')

# Create a Graph
G = nx.Graph()

def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_node_input(existing_nodes):
    while True:
        try:
            node_input = input("Enter node (format 'node_id,label'): ")
            node_id_str, label = node_input.split(',')
            node_id = int(node_id_str)
            if node_id in existing_nodes:
                print(f"Node ID {node_id} already exists. Please enter a unique node ID.")
                continue
            return node_id, label
        except ValueError:
            print("Invalid format. Please enter node in the format 'node_id,label'.")

def get_edge_input(nodes):
    while True:
        try:
            edge_input = input("Enter edge (format 'node1,node2'): ")
            node1_str, node2_str = edge_input.split(',')
            node1, node2 = int(node1_str), int(node2_str)
            if node1 not in nodes or node2 not in nodes:
                print(f"One or both nodes {node1} and {node2} are not valid nodes. Please enter valid nodes.")
                continue
            return node1, node2
        except ValueError:
            print("Invalid format. Please enter edge in the format 'node1,node2'.")

def get_color_limits(k):
    limits = []
    for i in range(k):
        while True:
            try:
                limit = int(input(f"Enter the maximum number of nodes for color {i+1}: "))
                limits.append(limit)
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")
    return limits

# Get the number of nodes and edges from the user
num_nodes = get_integer("How many nodes? ")
num_edges = get_integer("How many edges? ")

# Input nodes
existing_nodes = set()
for _ in range(num_nodes):
    node_id, label = get_node_input(existing_nodes)
    G.add_node(node_id, label=label)
    existing_nodes.add(node_id)

# Input edges
nodes = set(G.nodes())
for _ in range(num_edges):
    node1, node2 = get_edge_input(nodes)
    # Skip self-loops
    if node1 != node2:
        G.add_edge(node1, node2)

# Define color constraints
k = get_integer("Enter the number of colors: ")
color_limits = get_color_limits(k)

# Map colors to a palette
color_map = matplotlib.colormaps.get_cmap('tab10')  # Get the colormap

# Handle the color generation without division by zero
if k > 1:
    colors = [color_map(i / (k - 1)) for i in range(k)]  # Generate a list of k colors
else:
    colors = [color_map(0)]  # Only one color

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
