"""Algorytm Johnsona – najkrótsze ścieżki między wszystkimi parami wierzchołków."""

from bellman_ford import INF, bellman_ford
from dijkstra import dijkstra
from digraph import Digraph
import networkx as nx


def add_s(g, weights):
    """Tworzy G' przez dodanie nowego źródła s z krawędziami s -> v o wadze 0."""
    s = g.n + 1
    g_new = Digraph(g.n + 1)
    weights_new = {}

    for u, v in g.edges():
        g_new.add_edge(u, v)
        weights_new[(u, v)] = weights[(u, v)]

    for v in range(1, g.n + 1):
        g_new.add_edge(s, v)
        weights_new[(s, v)] = 0

    return g_new, weights_new, s


def _to_networkx(g, weights):
    graph_nx = nx.DiGraph()
    graph_nx.add_nodes_from(range(1, g.n + 1))
    for u, v in g.edges():
        graph_nx.add_edge(u, v, weight=weights[(u, v)])
    return graph_nx


def johnson(g, weights):
    """Zwraca macierz D (n x n) odległości najkrótszych ścieżek w grafie skierowanym.

    weights: słownik wag w postaci {(u, v): w} dla każdego łuku grafu g.
    Gdy graf zawiera cykl o ujemnej wadze, zgłaszany jest ValueError.
    """
    g_new, weights_new, s = add_s(g, weights)

    ds, _, cycle = bellman_ford(g_new, weights_new, s)
    if cycle is not None:
        raise ValueError("G zawiera cykl o ujemnej wadze.")

    h = ds
    reweighted = {}
    for u, v in g.edges():
        reweighted[(u, v)] = weights[(u, v)] + h[u] - h[v]
    reweighted_graph = _to_networkx(g, reweighted)

    d_matrix = [[INF] * g.n for _ in range(g.n)]
    for u in range(1, g.n + 1):
        du, _ = dijkstra(reweighted_graph, u)
        for v in range(1, g.n + 1):
            if du[v] != INF:
                d_matrix[u-1][v-1]=du[v]-h[u]+h[v]#nodes, tablica od 0 wiec -1

    return d_matrix
