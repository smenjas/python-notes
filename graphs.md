# Graphs in Python

[Graph theory](https://en.wikipedia.org/wiki/Graph_theory) is outside the scope of this document.

You can represent a graph as a dictionary of lists, where each key is a node, and each value is a list of connected nodes.
```python3
graph = {1: [2],
         2: [3, 4],
         3: [4, 5, 6],
         4: [1, 5],
         5: [2]}
```

## Resources
- [Python Patterns - Implementing Graphs](https://www.python.org/doc/essays/graphs/)
- [Graphs in Python](https://www.python-course.eu/graphs_python.php)
- [NetworkX](https://networkx.github.io/)
  - [NetworkX Stable Documentation](https://networkx.github.io/documentation/stable/)
