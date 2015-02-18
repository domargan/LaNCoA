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
import math

def reciprocity(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())

    self_loops = g.number_of_selfloops()
    r = sum([g.has_edge(e[1], e[0])
                    for e in g.edges_iter()]) / float(g.number_of_edges())

    a = (g.number_of_edges() - self_loops) / (float(g.number_of_nodes()) * float((g.number_of_nodes() - 1)))

    ro = float((r - a)) / float((1 - a))

    return r, a, ro


def entropy_in_degree(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())
    n = g.number_of_nodes()

    entropy = 0
    deg_sum = 0

    for i in g.nodes():
        deg_sum += g.in_degree(i)

    for i in g.nodes():
        if g.in_degree(i) > 0:
            entropy += ((g.in_degree(i) / float(deg_sum)) * (math.log(g.in_degree(i) / float(deg_sum))))

    entropy = -(entropy) / math.log(n)

    return entropy


def entropy_out_degree(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())
    n = g.number_of_nodes()

    entropy = 0
    deg_sum = 0

    for i in g.nodes():
        deg_sum += g.out_degree(i)

    for i in g.nodes():
        if g.out_degree(i) > 0:
            entropy += ((g.out_degree(i) / float(deg_sum)) * (math.log(g.out_degree(i) / float(deg_sum))))

    entropy = -(entropy) / math.log(n)

    return entropy


def entropy_degree(network):
    g = nx.read_weighted_edgelist(network)
    n = g.number_of_nodes()

    entropy = 0
    deg_sum = 0

    for i in g.nodes():
        deg_sum += g.degree(i)

    for i in g.nodes():
        if g.degree(i) > 0:
            entropy += ((g.degree(i) / float(deg_sum)) * (math.log(g.degree(i) / float(deg_sum))))

    entropy = -(entropy) / math.log(n)

    return entropy


def entropy_in_strenght(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())
    n = g.number_of_nodes()

    entropy = 0
    deg_sum = 0

    for i in g.nodes():
        deg_sum += g.in_degree(i, weight='weight')

    for i in g.nodes():
        if g.in_degree(i) > 0:
            entropy += ((g.in_degree(i, weight='weight') / float(deg_sum)) * (math.log(g.in_degree(i, weight='weight') / float(deg_sum))))

    entropy = -(entropy) / math.log(n)

    return entropy


def entropy_out_strenght(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())
    n = g.number_of_nodes()

    entropy = 0
    deg_sum = 0

    for i in g.nodes():
        deg_sum += g.out_degree(i, weight='weight')

    for i in g.nodes():
        if g.out_degree(i) > 0:
            entropy += ((g.out_degree(i, weight='weight') / float(deg_sum)) * (math.log(g.out_degree(i, weight='weight') / float(deg_sum))))

    entropy = -(entropy) / math.log(n)

    return entropy