from __future__ import annotations

from typing import Dict, List, Tuple, Optional
import heapq

from .graph import Graph


def dijkstra_shortest_path(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    """
    Compute shortest path from start to goal using Dijkstra's algorithm.

    This implementation validates that the graph has no negative-weight edges
    before running Dijkstra (Dijkstra cannot handle negative weights).
    """
    if graph.has_negative_weights():
        raise ValueError("Graph contains negative-weight edges; Dijkstra is unsafe")

    # Distances and predecessor tracking
    dist: Dict[str, float] = {start: 0.0}
    prev: Dict[str, Optional[str]] = {start: None}

    # Min-heap items: (cost, node)
    heap: List[Tuple[float, str]] = [(0.0, start)]

    while heap:
        cost, node = heapq.heappop(heap)

        # If a stale entry is popped, skip it
        if cost > dist.get(node, float("inf")):
            continue

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
    Bellman-Ford algorithm supporting negative-weight edges (but not negative cycles).
    Raises ValueError if a negative-weight cycle reachable from start exists or no path found.
    """
    # Initialize distances
    dist: Dict[str, float] = {node: float("inf") for node in graph.nodes()}
    prev: Dict[str, Optional[str]] = {node: None for node in graph.nodes()}

    if start not in dist:
        raise ValueError(f"Start node {start} not in graph")

    dist[start] = 0.0

    nodes = list(graph.nodes())
    n = len(nodes)

    # Relax edges up to n-1 times
    for _ in range(n - 1):
        updated = False
        for u, v, w in graph.edges():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                updated = True
        if not updated:
            break

    # Check for negative-weight cycles
    for u, v, w in graph.edges():
        if dist[u] + w < dist[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    if dist.get(goal, float("inf")) == float("inf"):
        raise ValueError(f"No path found from {start} to {goal}")

    return _reconstruct_path(prev, goal), dist[goal]


def shortest_path(graph: Graph, start: str, goal: str, algorithm: str = "auto") -> Tuple[List[str], float]:
    """Generic shortest-path entry point.

    algorithm: "auto" | "dijkstra" | "bellman-ford"
    - auto: use Bellman-Ford if negative weights present, otherwise Dijkstra
    - dijkstra: run Dijkstra (will reject graphs with negative weights)
    - bellman-ford: run Bellman-Ford
    """
    algo = algorithm.lower()
    if algo not in {"auto", "dijkstra", "bellman-ford"}:
        raise ValueError("algorithm must be 'auto', 'dijkstra' or 'bellman-ford'")

    if algo == "dijkstra":
        return dijkstra_shortest_path(graph, start, goal)

    if algo == "bellman-ford":
        return bellman_ford_shortest_path(graph, start, goal)

    # auto
    if graph.has_negative_weights():
        return bellman_ford_shortest_path(graph, start, goal)
    return dijkstra_shortest_path(graph, start, goal)


def _reconstruct_path(prev: Dict[str, Optional[str]], goal: str) -> List[str]:
    path: List[str] = []
    node = goal
    while node is not None:
        path.append(node)
        node = prev.get(node)
    return list(reversed(path))
