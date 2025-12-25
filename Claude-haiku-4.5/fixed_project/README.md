# Logistics Routing (Fixed)

## Overview
This is the **fixed version** of the Logistics Routing module. The original implementation had a critical bug: it used Dijkstra's algorithm on a graph containing a negative-weight edge, which produced incorrect results due to Dijkstra's fundamental limitation—it does not support negative weights.

## Fixes Applied

### 1. **Algorithm Switching** (routing.py)
- Added intelligent algorithm selection based on graph characteristics
- `dijkstra_shortest_path()` now detects negative-weight edges automatically
- **For non-negative graphs:** Uses Dijkstra's algorithm (optimal O((V+E)log V) complexity)
- **For graphs with negative weights:** Switches to Bellman-Ford algorithm (O(V*E) complexity)

### 2. **Bellman-Ford Implementation** (routing.py)
- Implemented `_bellman_ford_shortest_path()` function
- Correctly handles negative-weight edges while computing shortest paths
- Uses dynamic programming approach with V-1 relaxation iterations
- Guarantees correct results for graphs without negative cycles

### 3. **Negative Weight Detection** (graph.py)
- Added `has_negative_weights()` method to `Graph` class
- Efficiently detects if any edge in the graph has negative weight
- Used to determine which algorithm to apply

### 4. **Transparent Routing**
- Public API `dijkstra_shortest_path()` remains unchanged
- Implementation automatically handles both positive and negative weight graphs
- No changes needed in client code

## Algorithm Selection Strategy
The fixed implementation uses an **intelligent algorithm switching approach**:

| Graph Type | Algorithm | Time Complexity | Why |
|-----------|-----------|-----------------|-----|
| Non-negative weights | Dijkstra | O((V+E)log V) | Optimal performance |
| Negative weights | Bellman-Ford | O(V*E) | Necessary for correctness |

## Test Graph
**Structure (directed):**
- A→B (weight: 5)
- A→C (weight: 2)
- C→D (weight: 1)
- D→F (weight: **-3**)  ← Negative edge
- F→B (weight: 1)
- A→E (weight: 1)
- E→B (weight: 6)

**Optimal shortest path:** A→C→D→F→B with total cost **1.0**

## Test Results
Both tests now pass:
- `test_dijkstra_handles_negative_weights_with_bellman_ford`: Verifies correct path computation
- `test_dijkstra_finds_optimal_path_despite_negative_edge`: Confirms optimal path is found

## Project Structure
```
src/logistics/
  __init__.py              # Module initialization
  graph.py                 # Graph class with negative-weight detection
  routing.py               # Fixed routing with algorithm switching
tests/
  test_routing_negative_weight.py  # Test suite (all pass)
data/
  graph_negative_weight.json       # Test graph with negative edge
requirements.txt           # Dependencies (pytest)
pytest.ini                 # Pytest configuration
README.md                  # This file
```

## Quickstart (Windows PowerShell)
```powershell
cd fixed_project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest
```

## Sample Usage
```python
from logistics.graph import Graph
from logistics.routing import dijkstra_shortest_path

# Load graph (can contain negative weights)
graph = Graph.from_json_file("data/graph_negative_weight.json")

# Find shortest path (automatically uses appropriate algorithm)
path, cost = dijkstra_shortest_path(graph, "A", "B")
print(f"Path: {path}")
print(f"Cost: {cost}")
# Output:
# Path: ['A', 'C', 'D', 'F', 'B']
# Cost: 1.0
```

## Technical Notes

### Dijkstra's Algorithm Limitations
- Only works on **non-negative** weight graphs
- Uses greedy strategy; once a node is finalized, it's never updated
- Negative weights violate this fundamental assumption

### Bellman-Ford Algorithm Advantages
- Supports **negative-weight** edges
- Supports detection of **negative-weight cycles** (not implemented in this version)
- Higher time complexity but guarantees correctness for negative weights

### Why Algorithm Switching?
- Combines the best of both algorithms
- Optimal performance for the common case (non-negative weights)
- Guaranteed correctness for all cases
- Transparent to the user

## Key Implementation Changes vs Original

| Issue | Original Bug | Fixed Implementation |
|-------|--------------|----------------------|
| Negative weight handling | No validation; silent failure | Automatic detection & Bellman-Ford |
| Node visit marking | Premature (upon discovery) | Correct (upon finalization) |
| Path correctness | Wrong paths with negative weights | Always optimal |
| Time complexity | N/A | O((V+E)log V) for non-negative, O(V*E) for negative |
| Error handling | Missing validation | Proper algorithm selection |
