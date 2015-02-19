#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 Domagoj Margan <margan.domagoj@gmail.com>

This file is part of LaNCoA.
LaNCoA is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LaNCoA is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LaNCoA.  If not, see <http://www.gnu.org/licenses/>.
"""

import networkx as nx


def jaccard(network1, network2, d="directed"):
    if d == "directed":
        g1 = nx.read_weighted_edgelist(network1, create_using=nx.DiGraph())
        g2 = nx.read_weighted_edgelist(network2, create_using=nx.DiGraph())
    elif d == "undirected":
        g1 = nx.read_weighted_edgelist(network1)
        g2 = nx.read_weighted_edgelist(network2)

    union = nx.compose(g1, g2)
    inter = nx.intersection(g1, g2)

    j = float(inter.number_of_edges()) / float(union.number_of_edges())
    jd = 1 - j

    return j, jd


def total_overlap(network1, network2, d="directed"):
    if d == "directed":
        g1 = nx.read_weighted_edgelist(network1, create_using=nx.DiGraph())
        g2 = nx.read_weighted_edgelist(network2, create_using=nx.DiGraph())
    elif d == "undirected":
        g1 = nx.read_weighted_edgelist(network1)
        g2 = nx.read_weighted_edgelist(network2)

    overlap = 0
    for i in g1.edges():
        if g2.has_edge(i[0], i[1]):
            overlap += 1

    t_overlap = (float(overlap) / float(nx.compose(g1, g2).number_of_edges()))

    return t_overlap


def total_weighted_overlap(network1, network2, d="directed"):
    if d == "directed":
        g1 = nx.read_weighted_edgelist(network1, create_using=nx.DiGraph())
        g2 = nx.read_weighted_edgelist(network2, create_using=nx.DiGraph())
    elif d == "undirected":
        g1 = nx.read_weighted_edgelist(network1)
        g2 = nx.read_weighted_edgelist(network2)

    union = nx.compose(g1, g2)

    w_max_g1 = 0
    w_max_g2 = 0

    for (u,d,v) in g1.edges(data=True):
        if v['weight'] > w_max_g1:
            w_max_g1 = v['weight']

    for (u,d,v) in g2.edges(data=True):
        if v['weight'] > w_max_g2:
            w_max_g2 = v['weight']

    overall_weight = 0
    for (u,d,v) in union.edges(data=True):
        overall_weight += v['weight']

    sum_list = [min(float((g1.edge[u][d]['weight'] / w_max_g1)), float((g2.edge[u][d]['weight'] / w_max_g2)))
                for (u,d,v) in g1.edges(data=True) if g2.has_edge(u, d)]

    overlap = sum(sum_list)
    t_w_overlap = (float(overlap) / float(overall_weight))

    return t_w_overlap