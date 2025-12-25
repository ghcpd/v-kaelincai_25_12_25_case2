import pytest
from pathlib import Path

from logistics.graph import Graph
from logistics.routing import dijkstra_shortest_path

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "data" / "graph_negative_weight.json"


@pytest.fixture
def graph():
    return Graph.from_json_file(str(FIXTURE_PATH))


def test_dijkstra_handles_negative_weights(graph):
    """Expect the implementation to handle negative weights using Bellman-Ford."""
    path, cost = dijkstra_shortest_path(graph, "A", "B")
    assert path == ["A", "C", "D", "F", "B"]
    assert cost == pytest.approx(1.0)


def test_dijkstra_finds_optimal_path_despite_negative_edge(graph):
    """Even if allowed, the algorithm should find the optimal path (cost=1)."""
    path, cost = dijkstra_shortest_path(graph, "A", "B")
    assert path == ["A", "C", "D", "F", "B"]
    assert cost == pytest.approx(1.0)
