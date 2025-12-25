# Logistics Routing (Fixed Implementation)

## Overview
This Python module models a logistics routing system that correctly handles graphs with negative-weight edges. The implementation automatically selects the appropriate algorithm: Dijkstra for non-negative weights and Bellman-Ford for graphs containing negative weights.

## Scenario
**Graph (directed):**
- A→B (5)
- A→C (2)
- C→D (1)
- D→F (**-3**)
- F→B (1)
- A→E (1)
- E→B (6)

**Optimal Path:** `A→C→D→F→B` with total cost **1**.

## Project Structure
```
src/logistics/          # Core code
  graph.py              # Graph loader & helper (added has_negative_weights method)
  routing.py            # Corrected routing algorithms
tests/                  # Automated tests (now passing)
  test_routing_negative_weight.py
data/                  # Sample graph data
  graph_negative_weight.json
README.md              # This file
requirements.txt       # Dependencies (pytest)
pytest.ini             # Pytest config (pythonpath=src)
```

## Quickstart (Windows PowerShell)
```powershell
python -m venv .venv; .\.venv\Scripts\activate; pip install -r requirements.txt; pytest
```

## Sample Usage
```python
from logistics.graph import Graph
from logistics.routing import dijkstra_shortest_path

graph = Graph.from_json_file("data/graph_negative_weight.json")
path, cost = dijkstra_shortest_path(graph, "A", "B")
print(path, cost)  # ['A', 'C', 'D', 'F', 'B'] 1.0
```

## Algorithm Selection
- **Non-negative weights:** Uses corrected Dijkstra implementation (nodes marked visited when finalized).
- **Negative weights:** Uses Bellman-Ford algorithm (supports negative edges, detects negative cycles).

## Notes
- The function `dijkstra_shortest_path` automatically chooses the algorithm based on graph properties.
- Bellman-Ford has O(V×E) time complexity vs Dijkstra's O((V+E)logV), but is necessary for negative weights.</content>
<parameter name="filePath">c:\BugBash\workSpace1\grok-fast\fixed_project\README.md