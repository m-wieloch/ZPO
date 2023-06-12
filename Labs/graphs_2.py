#!/usr/bin/python
# -*- coding: utf-8 -*-

# Maciej Wieloch, 303080

from typing import List, Set, Dict, NamedTuple
import networkx as nx


# Pomocnicza definicja podpowiedzi typu reprezentującego etykietę
# wierzchołka (liczba 1..n).
# krawędzi i wagi
VertexID = int
EdgeID = int
WeightID = float

# Pomocnicza definicja podpowiedzi typu reprezentującego listę sąsiedztwa.
AdjList = Dict[VertexID, List[VertexID]]
Distance = int


# Nazwana krotka reprezentująca dystans od komórki startowej
class Vertex(NamedTuple):
    vertex_id: VertexID
    distance: Distance


# Nazwana krotka reprezentująca segment ścieżki.
class TrailSegmentEntry(NamedTuple):
    vertex_start: VertexID
    vertex_stop: VertexID
    edge_id: EdgeID
    weight: WeightID


# Trail
Trail = List[TrailSegmentEntry]


def neighbors(adjlist: AdjList, start_vertex_id: VertexID, max_distance: Distance) -> Set[VertexID]:

    if start_vertex_id not in adjlist:
        return None

    visited = []
    queue = Vertex([start_vertex_id], 0)

    cell_iterations = 1
    pending_dist = False

    while queue.vertex_id:
        u = queue.vertex_id.pop(0)
        cell_iterations = cell_iterations - 1

        for v in adjlist[u]:

            if v not in adjlist:
                adjlist[v] = []

            if v in adjlist and v not in visited:
                if pending_dist is True:
                    cell_iterations = len(adjlist[u])
                    pending_dist = False

                visited.append(v)
                queue.vertex_id.append(v)

        if cell_iterations == 0:
            queue = queue._replace(distance=queue.distance + 1)
            pending_dist = True

        if queue.distance == max_distance:
            break

    return set(visited)


def load_multigraph_from_file(filepath: str) -> nx.MultiDiGraph:
    """Stwórz multigraf na podstawie danych o krawędziach wczytanych z pliku.

    :param filepath: względna ścieżka do pliku (wraz z rozszerzeniem)
    :return: multigraf
    """
    with open(filepath) as f:
        list_of_edges = []

        for line in f:

            if line.strip():
                edge_element = line.split(" ")
                va = int(edge_element[0])
                vb = int(edge_element[1])
                w = float(edge_element[2])
                list_of_edges.append((va, vb, w))

            result = nx.MultiDiGraph()
            result.add_weighted_edges_from(list_of_edges)

        return result


def find_min_trail(g: nx.MultiDiGraph, v_start: VertexID, v_end: VertexID) -> Trail:
    """
    Znajdź najkrótszą ścieżkę w grafie pomiędzy zadanymi wierzchołkami.

    :param g: graf
    :param v_start: wierzchołek początkowy
    :param v_end: wierzchołek końcowy
    :return: najkrótsza ścieżka
    """
    def _find_min_trail(g: nx.MultiDiGraph, v_start: VertexID, v_end: VertexID) -> Trail:

        list_of_edges = g[v_start][v_end]
        edges_keys = list(list_of_edges.keys())
        shortest_edge_weight = g[v_start][v_end][0]['weight']
        shortest_edge_id = 0

        for i in edges_keys:
            edge_weight = g[v_start][v_end][i]['weight']

            if edge_weight < shortest_edge_weight:
                shortest_edge_weight = edge_weight
                shortest_edge_id = i

        result = TrailSegmentEntry(v_start, v_end, shortest_edge_id, shortest_edge_weight)

        return result

    path = nx.dijkstra_path(g, v_start, v_end)
    min_trail = []
    while len(path) > 1:
        u = path.pop(0)
        min_trail += [_find_min_trail(g, u, path[0])]

    return min_trail


def trail_to_str(trail: Trail) -> str:
    """Wyznacz reprezentację tekstową ścieżki.

    :param trail: ścieżka
    :return: reprezentacja tekstowa ścieżki
    1 -[0: 0.5]-> 2 -[1: 0.3]-> 3  (total = 0.8)
    """

    result = ''
    result = result + str(trail[0][0])
    total_weight = 0

    for i in range(0, len(trail)):
        result = result + ' -[' + str(trail[i][2]) + ': ' + str(trail[i][3]) + ']-> ' + str(trail[i][1])
        total_weight = total_weight + trail[i][3]

    result = result + '  (total = ' + str(total_weight) + ')'

    return result
