import pytest
from pathlib import Path

from logistics.graph import Graph
from logistics.routing import dijkstra_shortest_path, bellman_ford_shortest_path, shortest_path

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "data" / "graph_negative_weight.json"


@pytest.fixture
def graph():
    return Graph.from_json_file(str(FIXTURE_PATH))


def test_dijkstra_rejects_negative_weights(graph):
    """Expect Dijkstra to reject running on graphs with negative weights."""
    with pytest.raises(ValueError, match="negative"):
        dijkstra_shortest_path(graph, "A", "B")


def test_bellman_ford_finds_optimal_path_despite_negative_edge(graph):
    """Bellman-Ford should find the optimal path (cost=1)."""
    path, cost = bellman_ford_shortest_path(graph, "A", "B")
    assert path == ["A", "C", "D", "F", "B"]
    assert cost == pytest.approx(1.0)


def test_shortest_path_auto_chooses_bellman_ford(graph):
    """The auto chooser should pick Bellman-Ford and return the optimal path."""
    path, cost = shortest_path(graph, "A", "B", algorithm="auto")
    assert path == ["A", "C", "D", "F", "B"]
    assert cost == pytest.approx(1.0)
