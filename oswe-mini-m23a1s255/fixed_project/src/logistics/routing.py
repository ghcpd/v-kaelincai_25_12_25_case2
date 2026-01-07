from __future__ import annotations

from typing import Dict, List, Tuple, Optional
import heapq

from .graph import Graph


def dijkstra_shortest_path(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    """Dijkstra's algorithm for non-negative-weight graphs.

    This implementation:
    - Validates that there are no negative-weight edges and raises ValueError if any are found.
    - Finalizes (marks visited) a node only when it is popped from the priority queue.
    """
    if graph.has_negative_weights():
        raise ValueError("graph contains negative-weight edges; Dijkstra is unsafe")

    dist: Dict[str, float] = {start: 0.0}
    prev: Dict[str, Optional[str]] = {start: None}

    heap: List[Tuple[float, str]] = [(0.0, start)]
    visited = set()

    while heap:
        cost, node = heapq.heappop(heap)

        # Skip stale entries
        if cost > dist.get(node, float("inf")):
            continue

        # Finalize node when popped
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
    """Bellman-Ford algorithm supporting negative weights (no negative cycles reachable).

    Raises ValueError if a negative-weight cycle is detected that is reachable from start
    and can affect the path to the goal.
    """
    # Initialize
    dist: Dict[str, float] = {n: float("inf") for n in graph.nodes()}
    prev: Dict[str, Optional[str]] = {n: None for n in graph.nodes()}
    if start not in dist:
        raise ValueError(f"Start node {start} not in graph")
    dist[start] = 0.0

    nodes = list(graph.nodes())
    # Relax edges |V|-1 times
    for _ in range(len(nodes) - 1):
        updated = False
        for u in nodes:
            for v, w in graph.neighbors(u).items():
                if dist[u] + w < dist.get(v, float("inf")):
                    dist[v] = dist[u] + w
                    prev[v] = u
                    updated = True
        if not updated:
            break

    # Check for negative-weight cycles reachable from start
    for u in nodes:
        for v, w in graph.neighbors(u).items():
            if dist[u] + w < dist.get(v, float("inf")):
                raise ValueError("Graph contains a negative-weight cycle")

    if dist.get(goal, float("inf")) == float("inf"):
        raise ValueError(f"No path found from {start} to {goal}")

    return _reconstruct_path(prev, goal), dist[goal]


def shortest_path(graph: Graph, start: str, goal: str) -> Tuple[List[str], float]:
    """Convenience API: choose algorithm based on presence of negative weights."""
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
