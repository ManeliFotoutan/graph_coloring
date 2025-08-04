# Graph Coloring with Constraints

This project implements a graph coloring algorithm with constraints on the number of nodes that can share the same color. It uses **backtracking** to assign colors to nodes such that:
- No two adjacent nodes share the same color.
- The number of nodes assigned to each color does not exceed a specified limit.
  
 ##  Description

- The program prompts the user to enter the number of nodes and edges.
- Nodes are automatically labeled using capital letters (A, B, C, ...).
- Edges are entered in the format `node1_id,node2_id` (e.g., `0,1`).
- The user is then asked to define:
  - The number of colors available.
  - The maximum number of nodes allowed per color.
- The algorithm uses **depth-first search with backtracking** to find a valid coloring under these constraints.
- The resulting graph is saved as an image file named `graph_plot.png`.
  
For a detailed description of the algorithm, design decisions, and analysis, please refer to the [problem_coloring graph.pdf](./problem_coloring%20graph.pdf) file included in this repository.

##  Output

The output graph is saved as a PNG image with:
- Colored nodes representing their assigned color.
- Edge thickness fixed to a default value.
- Labels on each node for readability.

##  How to Run

1. Make sure you have Python 3 installed.
2. Install dependencies (if using virtual environments)
3.Run the script:
  python graph_coloring.py
Follow the prompts in the terminal to input graph structure and coloring constraints.

## Dependencies

You can install them manually if no requirements.txt is provided:
```bash
pip install networkx matplotlib
```

## Notes
Self-loops are ignored.
Only valid node indices are accepted.
The script uses matplotlib with the 'Agg' backend to allow non-interactive environments.

