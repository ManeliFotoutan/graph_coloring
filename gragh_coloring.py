import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

# Set the backend to 'Agg' for non-interactive environments
matplotlib.use('Agg')

def get_integer(prompt):
    """Get an integer input from the user."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_edge_input(nodes):
    """Get an edge input in the format 'node1,node2' from the user."""
    while True:
        try:
            edge_input = input("Enter edge (format 'node1_id,node2_id'): ")
            node1_str, node2_str = edge_input.split(',')
            node1, node2 = int(node1_str), int(node2_str)
            if node1 not in nodes or node2 not in nodes:
                print(f"One or both nodes {node1} and {node2} are not valid nodes. Please enter valid nodes.")
                continue
            return node1, node2
        except ValueError:
            print("Invalid format. Please enter edge in the format 'node1_id,node2_id'.")

def get_color_limits(k):
    """Get the maximum number of nodes that can be assigned to each color."""
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

def is_safe(node, color, color_assignment, G, color_limits, color_count):
    """Check if the current color assignment is safe."""
    # Check adjacent nodes
    for neighbor in G.neighbors(node):
        if color_assignment.get(neighbor) == color:
            return False
    # Check color limits
    if color_count[color] >= color_limits[color]:
        return False
    return True

def graph_coloring(G, color_assignment, color_count, color_limits, colors, node_list, index):
    """Utilize backtracking to color the graph."""
    if index == len(node_list):
        return True  # All nodes are colored

    node = node_list[index]

    for color in range(len(colors)):
        if is_safe(node, color, color_assignment, G, color_limits, color_count):
            # Assign color
            color_assignment[node] = color
            color_count[color] += 1

            # Recur to assign colors to the next node
            if graph_coloring(G, color_assignment, color_count, color_limits, colors, node_list, index + 1):
                return True

            # If assigning color doesn't lead to a solution, remove it (backtrack)
            color_assignment[node] = -1
            color_count[color] -= 1

    return False

# Create a Graph
G = nx.Graph()

# Get the number of nodes and edges from the user
num_nodes = get_integer("How many nodes? ")
num_edges = get_integer("How many edges? ")

# Automatically generate nodes with IDs and labels like A, B, C, ...
for node_id in range(num_nodes):
    label = chr(65 + node_id)  # Convert node_id to corresponding ASCII uppercase letter
    G.add_node(node_id, label=label)

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
max_colors = color_map.N  # Number of colors in the colormap

# Handle the color generation without division by zero
if k > 1:
    colors = [color_map(i / max(max_colors - 1, 1)) for i in range(k)]  # Generate a list of k colors
else:
    colors = [color_map(0)]  # Only one color

# Initialize color assignment
color_assignment = {node: -1 for node in G.nodes()}
color_count = [0] * k  # Count of nodes assigned to each color

# Get the list of nodes
node_list = list(G.nodes())

# Start coloring using backtracking
if not graph_coloring(G, color_assignment, color_count, color_limits, colors, node_list, 0):
    raise ValueError("No valid coloring exists with the given constraints.")

# Apply the colors to the nodes
node_colors = {node: colors[color_assignment[node]] for node in G.nodes()}

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
plt.title("Graph Coloring")
plt.savefig('graph_plot.png')  # Save as PNG file
plt.close()  # Close the plot to free up resources


# def is_multigraph(G):
#     """Check if the graph is a multigraph."""
#     return isinstance(G, nx.MultiGraph)

# def remove_loops(G):
#     """Remove self-loops from the graph."""
#     loops = list(nx.selfloop_edges(G))
#     G.remove_edges_from(loops)
#     if loops:
#         print(f"Removed {len(loops)} self-loop(s).")
#     return G

# def remove_multiple_edges(G):
#     """Convert multigraph to simple graph by removing multiple edges."""
#     if is_multigraph(G):
#         simple_G = nx.Graph()
#         for u, v, data in G.edges(data=True):
#             if simple_G.has_edge(u, v):
#                 continue  # Skip additional edges
#             simple_G.add_edge(u, v, **data)
#         return simple_G
#     return G

# def convert_to_simple_graph(G):
#     """Convert any graph to a simple graph."""
#     G = remove_loops(G)
#     G = remove_multiple_edges(G)
#     return G

# Create a Graph
#G = nx.Graph()
# G = convert_to_simple_graph(G)