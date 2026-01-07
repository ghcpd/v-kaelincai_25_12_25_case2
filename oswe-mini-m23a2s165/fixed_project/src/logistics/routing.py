from __future__ import annotations

from typing import Dict, List, Tuple, Optional
import heapq

from .graph import Graph


def dijkstra_shortest_path(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    """
    Dijkstra's algorithm that validates input and works only for graphs without
    negative-weight edges. If negative weights are present this function raises
    ValueError to prevent incorrect results.
    """
    if graph.has_negative_weights():
        raise ValueError("Graph contains negative-weight edges; Dijkstra is not applicable")

    # Distances and predecessor tracking
    dist: Dict[str, float] = {start: 0.0}
    prev: Dict[str, Optional[str]] = {start: None}

    # Min-heap items: (cost, node)
    heap: List[Tuple[float, str]] = [(0.0, start)]

    # Visited set is used to mark nodes once they are popped (finalized)
    visited = set()

    while heap:
        cost, node = heapq.heappop(heap)

        # Skip stale entries
        if cost > dist.get(node, float("inf")):
            continue

        # Mark node as finalized
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return _reconstruct_path(prev, goal), cost

        for neighbor, weight in graph.neighbors(node).items():
            new_cost = cost + weight
            if new_cost < dist.get(neighbor, float("inf")):
                dist[neighbor] = new_cost
                prev[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))

    raise ValueError(f"No path found from {start} to {goal}")


def bellman_ford_shortest_path(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    """
    Bellman-Ford implementation to support graphs with negative-weight edges
    (but not negative-weight cycles). Raises ValueError if a negative cycle is
    detected or if no path exists.
    """
    # Initialize distances
    dist: Dict[str, float] = {n: float("inf") for n in graph.nodes()}
    prev: Dict[str, Optional[str]] = {n: None for n in graph.nodes()}
    if start not in dist:
        raise ValueError(f"Start node {start} not in graph")
    dist[start] = 0.0

    nodes = list(graph.nodes())
    # Relax edges repeatedly
    for _ in range(len(nodes) - 1):
        updated = False
        for u in nodes:
            for v, w in graph.neighbors(u).items():
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    updated = True
        if not updated:
            break

    # Check for negative-weight cycles
    for u in nodes:
        for v, w in graph.neighbors(u).items():
            if dist[u] + w < dist[v]:
                raise ValueError("Graph contains a negative-weight cycle")

    if dist.get(goal, float("inf")) == float("inf"):
        raise ValueError(f"No path found from {start} to {goal}")

    return _reconstruct_path(prev, goal), dist[goal]


def _reconstruct_path(prev: Dict[str, Optional[str]], goal: str) -> List[str]:
    path: List[str] = []
    node = goal
    while node is not None:
        path.append(node)
        node = prev.get(node)
    return list(reversed(path))
