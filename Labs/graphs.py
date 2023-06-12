#!/usr/bin/python
# -*- coding: utf-8 -*-

# Maciej Wieloch, 303080

from typing import Dict, List


def adjmat_to_adjlist(adjmat: List[List[int]]) -> Dict[int, List[int]]:

    mylist = []
    mydict = {}

    for idx, val in enumerate(adjmat):

        for idx2, val2 in enumerate(val):

            for i in range(val2):
                mylist.append(idx2+1)

        if mylist:
            mydict[idx+1] = mylist
            mylist = []

    return mydict


def dfs_recursive(g: Dict[int, List[int]], s: int) -> List[int]:

    """
    procedure DFS-recursive(G, v, visited):
    oznacz v jako odwiedzony
    dla każdego wierzchołka u będącego sąsiadem wierzchołka v:
        jeżeli u nieodwiedzony:
            DFS-recursive(G, u, visited)
    """

    def _dfs_recursive(gin: Dict[int, List[int]], v: int, visited: List[int]):
        if v in gin:
            visited.append(v)

            for i in gin[v]:

                if i not in visited:
                    _dfs_recursive(gin, i, visited)

    result = []
    _dfs_recursive(g, s, result)
    return result


def dfs_iterative(g: Dict[int, List[int]], s: int) -> List[int]:

    """
    procedure DFS-iterative(G, v):
    utwórz stos S
    odłóż v na S
    dopóki S nie jest pusty:
        zdejmij v z S   // czyli: zapamiętaj element ściągnięty ze stosu S w zmiennej v
        jeśli v nieodwiedzony:
            oznacz v jako odwiedzony
            dla każdego wierzchołka u będącego sąsiadem wierzchołka v:
                odłóż u na S
    """

    result = []
    stack = [s]

    while stack:

        v = stack.pop(0)

        if v not in result:
            result.append(v)
            stack = [u for u in g[v] if u in g] + stack

    return result


def is_acyclic(g: Dict[int, List[int]]) -> bool:

    """
    sprawdz czy sasiad wierzcholka zostal odwiedzony - cykl
    zapamietaj wierzcholki odwiedzonej aktualnej galezi
    """

    stack = [iter(g)]
    visited = set()

    result = [object()]
    result_set = set(result)

    while stack:

        for v in stack[-1]:

            if v in result_set:
                return False

            elif v not in visited:
                visited.add(v)
                result.append(v)
                result_set.add(v)
                stack.append(iter(g.get(v, ())))
                break

        else:
            result_set.remove(result.pop())
            stack.pop()

    return True
