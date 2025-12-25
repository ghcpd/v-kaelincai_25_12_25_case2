# Project Fix Task

## Problem Project Overview

This project is a Logistics Routing system that suffers from **incorrect algorithm selection and missing input validation**. The code forces the use of Dijkstra's algorithm on a graph containing negative-weight edges, resulting in suboptimal paths instead of the true shortest path.

## Project File Structure

```
issue_project/
├── README.md                                    # Project documentation
├── KNOWN_ISSUE.md                               # Detailed issue analysis
├── requirements.txt                             # Dependencies (pytest==7.4.4)
├── pytest.ini                                   # Pytest configuration
├── data/
│   └── graph_negative_weight.json              # Graph data with negative weights
├── src/
│   └── logistics/
│       ├── __init__.py                         # Module initialization
│       ├── graph.py                            # Graph data structure and loader
│       └── routing.py                          # Routing algorithm (buggy)
└── tests/
    └── test_routing_negative_weight.py         # Test file (currently failing)
```

## Core Problem Description

### Problem Manifestation

**Test Graph Structure (Directed):**
```
A → B (weight: 5)
A → C (weight: 2)
C → D (weight: 1)
D → F (weight: -3)  ← Negative weight edge
F → B (weight: 1)
A → E (weight: 1)
E → B (weight: 6)
```

**Path from A to B:**
- **Theoretically Optimal Path**: `A → C → D → F → B`, Total Cost = **1**
  - A→C: 2
  - C→D: 1
  - D→F: -3
  - F→B: 1
  - Total: 2 + 1 + (-3) + 1 = 1

- **Actually Returned Path**: `A → B`, Total Cost = **5** (Wrong!)

### Root Cause

1. **Algorithm Precondition Violation**:
   - Dijkstra's algorithm **does not support negative-weight edges**, but the code doesn't check for negative weights in the graph
   - When negative weights exist, Dijkstra produces incorrect results

2. **Implementation Bug** (routing.py):
   - **Premature Visit Marking**: Nodes are marked as visited when discovered (line 23), not when popped from the priority queue
   - This prevents re-relaxation of visited nodes even when a better path is found
   - Code snippet:
     ```python
     visited = set([start])  # Mark start node immediately
     ...
     visited.add(neighbor)   # Mark neighbor immediately upon discovery, not finalization
     ```

3. **Missing Input Validation**:
   - No check for negative-weight edges before running Dijkstra
   - No alternative algorithm provided for graphs with negative weights (e.g., Bellman-Ford)

### Test Failures

Both tests will fail:

1. `test_dijkstra_rejects_negative_weights`: Expects `ValueError` to be raised when negative weights are detected
2. `test_dijkstra_finds_optimal_path_despite_negative_edge`: Expects optimal path `["A", "C", "D", "F", "B"]` with cost `1.0`

## Fix Requirements

### 1. Output Directory Structure

Please create a new subdirectory for the fixed project. **Do NOT modify the original `issue_project` directory**.

Recommended fixed project directory structure:

```
└── fixed_project/                              # Fixed project (CREATE THIS)
    ├── README.md                               # Updated documentation explaining fix
    ├── requirements.txt                        # Dependencies
    ├── pytest.ini                              # Pytest configuration
    ├── data/
    │   └── graph_negative_weight.json         # Test graph data
    ├── src/
    │   └── logistics/
    │       ├── __init__.py                    # Module initialization
    │       ├── graph.py                       # Graph data structure
    │       └── routing.py                     # Fixed routing algorithm
    └── tests/
        └── test_routing_negative_weight.py    # Fixed tests (should pass)
```

### 2. Fix Objectives

- **Add Input Validation**: Detect negative-weight edges before running Dijkstra
- **Fix Dijkstra Implementation**: Correctly handle node visit marking (mark when finalized, not when discovered)
- **Provide Alternative Solution**: For graphs with negative weights, either reject with error or implement Bellman-Ford algorithm
- **Pass All Tests**: Fixed implementation should pass both test cases

### 3. Files That Need Fixing

1. **src/logistics/routing.py**
   - Add negative weight detection logic
   - Fix node visit marking timing in Dijkstra algorithm
   - Optional: Implement Bellman-Ford algorithm as alternative for negative-weight graphs

2. **src/logistics/graph.py** (Optional)
   - Can add helper method to detect negative weights in graph
   - Example: `has_negative_weights()` method

3. **tests/test_routing_negative_weight.py** (May need adjustment)
   - Depending on fix approach, test expectations may need adjustment
   - If choosing error-raising approach, keep first test
   - If implementing Bellman-Ford, keep second test

4. **README.md**
   - Update documentation to explain issue is fixed
   - Describe fix approach (validation/rejection or algorithm replacement)

### 4. Fix Approach Options

You can choose one of the following approaches:

**Approach A: Validate and Reject**
- Scan all edges at the start of `dijkstra_shortest_path`
- If any negative-weight edge is found, raise `ValueError`
- Fix visit marking issue in Dijkstra implementation

**Approach B: Algorithm Switching**
- Implement Bellman-Ford algorithm (supports negative weights)
- Automatically switch to Bellman-Ford when negative weights detected
- Or provide two separate functions for user selection

**Approach C: Fix Dijkstra + Validation**
- Fix Dijkstra implementation issue (visit marking)
- Add negative weight validation
- Clearly document algorithm limitations

### 5. Constraints

- **Do NOT provide specific implementation code**: Only point out where problems are and the direction for fixes
- **Keep API Clear**: Function signatures should be clear and understandable
- **Ensure Tests Pass**: After fixing, at least one test should pass
- **Complete Documentation**: Explain algorithm applicability conditions and limitations

## Fix Verification

After fixing, you should be able to:

1. Run `pytest` and pass at least one test (depending on chosen fix approach)
2. For graphs with negative weights, either return correct shortest path or raise clear error
3. For graphs without negative weights, Dijkstra algorithm works normally
4. Code behavior is predictable and documented

## Technical Background

**Dijkstra Algorithm Limitations**:
- Only works on non-negative weight graphs
- Uses greedy strategy; once a node is finalized, it's never updated
- Negative weights violate this assumption

**Bellman-Ford Algorithm**:
- Supports negative-weight edges (but not negative-weight cycles)
- Higher time complexity: O(V×E) vs Dijkstra's O((V+E)logV)
- Can detect negative-weight cycles

## Task Description

Please analyze the problematic project described above, fix the errors in the routing algorithm, and create a complete fixed project in the `fixed_project` directory. Ensure the fixed code correctly handles negative-weight edges and passes the corresponding tests.
