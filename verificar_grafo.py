#!/usr/bin/env python3
"""Verifica estadísticas del grafo AS-CAIDA desde archivo MTX."""

from __future__ import annotations

import sys
from pathlib import Path


def load_mtx(path: Path) -> tuple[int, list[tuple[int, int]]]:
    edges: list[tuple[int, int]] = []
    n_nodes = 0
    with path.open() as f:
        for line in f:
            if line.startswith("%"):
                continue
            parts = line.split()
            if len(parts) == 3 and not edges:
                n_nodes = int(parts[0])
                continue
            if len(parts) >= 2:
                u, v = int(parts[0]), int(parts[1])
                if u != v:
                    edges.append((u, v))
    return n_nodes, edges


def build_graph(n_nodes: int, edges: list[tuple[int, int]]):
    try:
        import networkx as nx

        g = nx.Graph()
        g.add_nodes_from(range(1, n_nodes + 1))
        g.add_edges_from(edges)
        return ("networkx", g)
    except ImportError:
        adj: list[set[int]] = [set() for _ in range(n_nodes + 1)]
        for u, v in edges:
            adj[u].add(v)
            adj[v].add(u)
        return ("adjacency", adj)


def compute_stats(graph_kind: str, graph) -> dict[str, float | int]:
    if graph_kind == "networkx":
        import networkx as nx

        g = graph
        degrees = [d for _, d in g.degree()]
        cores = nx.core_number(g)
        return {
            "nodos": g.number_of_nodes(),
            "aristas": g.number_of_edges(),
            "grado_promedio": sum(degrees) / len(degrees),
            "grado_maximo": max(degrees),
            "clustering": nx.average_clustering(g),
            "k_core_maximo": max(cores.values()),
        }

    adj = graph
    n_nodes = len(adj) - 1
    degrees = [len(adj[i]) for i in range(1, n_nodes + 1)]

    clustering_sum = 0.0
    for i in range(1, n_nodes + 1):
        k = len(adj[i])
        if k < 2:
            continue
        neighbors = adj[i]
        edges_among = 0
        for u in neighbors:
            edges_among += len(neighbors & adj[u])
        edges_among //= 2
        clustering_sum += (2 * edges_among) / (k * (k - 1))

    return {
        "nodos": n_nodes,
        "aristas": sum(degrees) // 2,
        "grado_promedio": sum(degrees) / n_nodes,
        "grado_maximo": max(degrees),
        "clustering": clustering_sum / n_nodes,
        "k_core_maximo": -1,
    }


def main() -> int:
    path = Path(__file__).with_name("tech-as-caida2007.mtx")
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])

    if not path.exists():
        print(f"Archivo no encontrado: {path}")
        return 1

    n_header, edges = load_mtx(path)
    graph_kind, graph = build_graph(n_header, edges)
    results = compute_stats(graph_kind, graph)

    if results["k_core_maximo"] == -1:
        print("Instala networkx para calcular k-core: pip install networkx")
        return 1

    expected = {
        "nodos": 26475,
        "aristas": 53381,
        "grado_promedio": 4.033,
        "grado_maximo": 2628,
        "clustering": 0.208,
        "k_core_maximo": 22,
    }

    print(f"Archivo: {path.name}")
    print(f"Motor: {graph_kind}")
    print(f"Formato: Matrix Market simétrico (grafo no dirigido)\n")
    print(f"{'Métrica':<22} {'Calculado':>12} {'Esperado':>12} {'OK':>6}")
    print("-" * 56)

    all_ok = True
    for key, exp in expected.items():
        val = results[key]
        if key in {"grado_promedio", "clustering"}:
            ok = abs(float(val) - float(exp)) < 0.01
            disp = f"{float(val):.3f}"
            exp_disp = f"{float(exp):.3f}"
        else:
            ok = val == exp
            disp = str(val)
            exp_disp = str(exp)
        all_ok &= ok
        mark = "✓" if ok else "✗"
        print(f"{key:<22} {disp:>12} {exp_disp:>12} {mark:>6}")

    print("-" * 56)
    print("Resultado:", "COINCIDE" if all_ok else "HAY DIFERENCIAS")
    print("\nNota: Network Repository reporta grado máximo 2.6K y k-core 23;")
    print("este archivo .mtx verifica 2628 y k-core 22.")
    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
