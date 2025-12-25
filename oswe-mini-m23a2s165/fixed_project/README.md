Fixed logistics routing project.

- dijkstra_shortest_path now validates for negative-weight edges and raises ValueError if any are present.
- Bellman–Ford implementation `bellman_ford_shortest_path` added to support negative-weight edges (no negative cycles in test data).
- Graph helper `has_negative_weights` added.
