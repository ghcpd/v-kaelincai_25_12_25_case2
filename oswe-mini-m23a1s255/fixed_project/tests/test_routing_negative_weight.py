import pytest
from pathlib import Path

from logistics.graph import Graph
from logistics.routing import dijkstra_shortest_path, shortest_path

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "data" / "graph_negative_weight.json"


@pytest.fixture
def graph():
    return Graph.from_json_file(str(FIXTURE_PATH))


def test_dijkstra_rejects_negative_weights(graph):
    """Dijkstra must refuse to run on graphs with negative weights."""
    with pytest.raises(ValueError, match="negative"):
        dijkstra_shortest_path(graph, "A", "B")


def test_shortest_path_chooses_algorithm_and_finds_optimal(graph):
    """High-level shortest_path should handle negative edges and return optimal path."""
    path, cost = shortest_path(graph, "A", "B")
    assert path == ["A", "C", "D", "F", "B"]
    assert cost == pytest.approx(1.0)
