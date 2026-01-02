# Logistics Routing (Fixed Project)

## Overview
This fixed project resolves two issues in the original implementation:

- Dijkstra was used even when the graph contained negative-weight edges (invalid precondition).
- Dijkstra implementation prematurely marked nodes as finalized when discovered, preventing correct re-relaxation.

Fix decisions:

- A `Graph.has_negative_weights()` helper was added to detect negative edges.
- `dijkstra_shortest_path` now validates and *rejects* graphs that contain negative weights with a clear error.
- A Bellman-Ford implementation `bellman_ford_shortest_path` was added to correctly handle negative-weight edges.
- A convenience `shortest_path(..., algorithm="auto")` function automatically selects Bellman-Ford when negative weights are present and Dijkstra otherwise.

## Usage
- Use `dijkstra_shortest_path` only on graphs with non-negative weights.
- Use `bellman_ford_shortest_path` or `shortest_path(..., algorithm="auto")` for graphs that may contain negative edges.

## Tests
- `tests/test_routing_negative_weight.py` verifies that:
  - Dijkstra rejects graphs with negative weights
  - Bellman-Ford finds the optimal path through a negative-weight edge
  - The auto chooser selects Bellman-Ford when needed

## Quickstart
```powershell
python -m venv .venv; .\.venv\Scripts\activate; pip install -r requirements.txt; pytest
```
