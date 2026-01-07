Fixed logistics routing project.

Fix summary:
- Dijkstra implementation corrected (nodes finalized on pop, not on discovery)
- Negative-weight detection added to Graph
- Dijkstra now rejects graphs with negative weights
- Bellman-Ford implemented and used automatically when negative edges exist

How to run tests:

> python -m pip install -r requirements.txt
> python -m pytest -q
