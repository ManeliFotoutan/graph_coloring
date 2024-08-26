import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

# Set the backend to 'Agg' for non-interactive environments
matplotlib.use('Agg')


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

def get_color_names(k):
    while True:
        color_names = input(f"Enter {k} colors separated by spaces (e.g., 'red blue green ...'): ").split()
        if len(color_names) != k:
            print(f"Please enter exactly {k} colors.")
            continue
        try:
            # Validate color names by converting them to RGB values using Matplotlib
            colors = [matplotlib.colors.to_rgb(name) for name in color_names]
            return colors
        except ValueError as e:
            print(f"Invalid color name: {e}. Please try again.")


def is_multigraph(G):
    """Check if the graph is a multigraph."""
    return isinstance(G, nx.MultiGraph)

def remove_loops(G):
    """Remove self-loops from the graph."""
    loops = list(nx.selfloop_edges(G))
    G.remove_edges_from(loops)
    if loops:
        print(f"Removed {len(loops)} self-loop(s).")
    return G

def remove_multiple_edges(G):
    """Convert multigraph to simple graph by removing multiple edges."""
    if is_multigraph(G):
        simple_G = nx.Graph()
        for u, v, data in G.edges(data=True):
            if simple_G.has_edge(u, v):
                continue  # Skip additional edges
            simple_G.add_edge(u, v, **data)
        return simple_G
    return G

def convert_to_simple_graph(G):
    """Convert any graph to a simple graph."""
    G = remove_loops(G)
    G = remove_multiple_edges(G)
    return G

# Create a Graph
G = nx.Graph()
G = convert_to_simple_graph(G)

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


# Get color names from the user
colors = get_color_names(k)  # This replaces the previous automatic color map
# Map colors to a palette
color_map = matplotlib.colormaps.get_cmap('tab10')  # Get the colormap

# Handle the color generation without division by zero
if k > 1:
    colors = [color_map(i / (k - 1)) for i in range(k)]  # Generate a list of k colors
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
plt.title("Graph with User Input")
plt.savefig('graph_plot.png')  # Save as PNG file
plt.close()  # Close the plot to free up resources