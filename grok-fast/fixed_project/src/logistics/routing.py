from __future__ import annotations

from typing import Dict, List, Tuple, Optional
import heapq

from .graph import Graph


def dijkstra_shortest_path(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    """
    Compute shortest path from start to goal using Dijkstra or Bellman-Ford as appropriate.

    If the graph has negative weights, uses Bellman-Ford algorithm.
    Otherwise, uses corrected Dijkstra implementation.
    """
    if graph.has_negative_weights():
        return bellman_ford_shortest_path(graph, start, goal)
    else:
        return _dijkstra_shortest_path(graph, start, goal)


def _dijkstra_shortest_path(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    """
    Compute shortest path using corrected Dijkstra implementation.
    Nodes are marked visited only when finalized (popped from heap).
    """
    # Distances and predecessor tracking
    dist: Dict[str, float] = {node: float("inf") for node in graph.nodes()}
    dist[start] = 0.0
    prev: Dict[str, Optional[str]] = {node: None for node in graph.nodes()}

    # Min-heap items: (cost, node)
    heap: List[Tuple[float, str]] = [(0.0, start)]

    visited = set()

    while heap:
        cost, node = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)  # Mark as visited when finalized

        if node == goal:
            return _reconstruct_path(prev, goal), cost

        for neighbor, weight in graph.neighbors(node).items():
            if neighbor in visited:
                continue
            new_cost = cost + weight
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                prev[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))

    raise ValueError(f"No path found from {start} to {goal}")


def bellman_ford_shortest_path(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    """
    Compute shortest path using Bellman-Ford algorithm.
    Supports negative weights but detects negative cycles.
    """
    # Initialize distances
    dist: Dict[str, float] = {node: float("inf") for node in graph.nodes()}
    dist[start] = 0.0
    prev: Dict[str, Optional[str]] = {node: None for node in graph.nodes()}

    # Relax edges |V| - 1 times
    for _ in range(len(dist) - 1):
        for node in graph.nodes():
            for neighbor, weight in graph.neighbors(node).items():
                if dist[node] != float("inf") and dist[node] + weight < dist[neighbor]:
                    dist[neighbor] = dist[node] + weight
                    prev[neighbor] = node

    # Check for negative cycles
    for node in graph.nodes():
        for neighbor, weight in graph.neighbors(node).items():
            if dist[node] != float("inf") and dist[node] + weight < dist[neighbor]:
                raise ValueError("Graph contains a negative-weight cycle")

    if dist[goal] == float("inf"):
        raise ValueError(f"No path found from {start} to {goal}")

    return _reconstruct_path(prev, goal), dist[goal]


def _reconstruct_path(prev: Dict[str, Optional[str]], goal: str) -> List[str]:
    path: List[str] = []
    node = goal
    while node is not None:
        path.append(node)
        node = prev.get(node)
    return list(reversed(path))