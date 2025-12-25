from __future__ import annotations

from typing import Dict, List, Tuple, Optional
import heapq

from .graph import Graph


def dijkstra_shortest_path(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    """
    Compute shortest path from start to goal using Dijkstra's algorithm for non-negative
    graphs or Bellman-Ford for graphs with negative weights.

    FIXED: Now includes negative-weight detection and switches to Bellman-Ford when needed.
    
    Args:
        graph: A directed weighted graph
        start: Starting node
        goal: Goal node
    
    Returns:
        A tuple of (path: List[str], cost: float)
        
    Raises:
        ValueError: If no path exists from start to goal
    """
    # FIX: Use Bellman-Ford if graph has negative weights, otherwise use Dijkstra
    if graph.has_negative_weights():
        return _bellman_ford_shortest_path(graph, start, goal)
    else:
        return _dijkstra_shortest_path(graph, start, goal)


def _dijkstra_shortest_path(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    """
    Dijkstra's algorithm for shortest path on non-negative weight graphs.
    
    Time complexity: O((V+E)logV)
    """
    # Distances and predecessor tracking
    dist: Dict[str, float] = {node: float("inf") for node in graph.nodes()}
    dist[start] = 0.0
    prev: Dict[str, Optional[str]] = {node: None for node in graph.nodes()}

    # Min-heap items: (cost, node)
    heap: List[Tuple[float, str]] = [(0.0, start)]

    # FIX: Mark nodes visited only when they are finalized (popped from heap)
    visited = set()

    while heap:
        cost, node = heapq.heappop(heap)

        # If node already visited, skip (it was already finalized)
        if node in visited:
            continue

        # Finalize this node
        visited.add(node)

        if node == goal:
            return _reconstruct_path(prev, goal), cost

        # If a stale entry is popped, skip it
        if cost > dist.get(node, float("inf")):
            continue

        for neighbor, weight in graph.neighbors(node).items():
            # Only relax edges to unvisited nodes
            if neighbor not in visited:
                new_cost = cost + weight
                if new_cost < dist.get(neighbor, float("inf")):
                    dist[neighbor] = new_cost
                    prev[neighbor] = node
                    heapq.heappush(heap, (new_cost, neighbor))

    raise ValueError(f"No path found from {start} to {goal}")


def _bellman_ford_shortest_path(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    """
    Bellman-Ford algorithm for shortest path on graphs with negative weights.
    
    Time complexity: O(V*E)
    Supports negative weights but not negative cycles.
    """
    nodes = list(graph.nodes())
    
    # Initialize distances and predecessors
    dist: Dict[str, float] = {node: float("inf") for node in nodes}
    dist[start] = 0.0
    prev: Dict[str, Optional[str]] = {node: None for node in nodes}

    # Relax edges V-1 times
    for _ in range(len(nodes) - 1):
        for node in nodes:
            if dist[node] == float("inf"):
                continue
            for neighbor, weight in graph.neighbors(node).items():
                new_cost = dist[node] + weight
                if new_cost < dist[neighbor]:
                    dist[neighbor] = new_cost
                    prev[neighbor] = node

    # Check for negative cycles (optional, not needed for this problem)
    # In a real implementation, you might want to detect and report negative cycles

    if dist[goal] == float("inf"):
        raise ValueError(f"No path found from {start} to {goal}")

    return _reconstruct_path(prev, goal), dist[goal]


def _reconstruct_path(prev: Dict[str, Optional[str]], goal: str) -> List[str]:
    """Reconstruct path from start to goal using predecessor links."""
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    return path
