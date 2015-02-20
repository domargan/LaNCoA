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


def in_selectivity(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())

    selectivity_dict = {}
    for node in g.nodes():
        s = g.in_degree(node, weight='weight')
        k = g.in_degree(node, weight=None)
        if k > 0:
            selectivity = s / k
            selectivity_dict[node] = selectivity
        else:
            selectivity_dict[node] = 0

    return selectivity_dict


def out_selectivity(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())

    selectivity_dict = {}
    for node in g.nodes():
        s = g.out_degree(node, weight='weight')
        k = g.out_degree(node, weight=None)
        if k > 0:
            selectivity = s / k
            selectivity_dict[node] = selectivity
        else:
            selectivity_dict[node] = 0

    return selectivity_dict


def selectivity(network):
    g = nx.read_weighted_edgelist(network)

    selectivity_dict = {}
    for node in g.nodes():
        s = g.degree(node, weight='weight')
        k = g.degree(node, weight=None)
        if k > 0:
            selectivity = s / k
            selectivity_dict[node] = selectivity
        else:
            selectivity_dict[node] = 0

    return selectivity_dict


def in_ipr(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())

    inv_part_dict = {}
    for node in g.nodes():
        s = g.in_degree(node, weight='weight')
        predcessors = g.predecessors(node)
        if (len(predcessors) == 0 and s == 0):
            inv_part_dict[node] = 0
        else:
            sum_list = []
            for in_node in predcessors:
                a = g.edge[in_node][node]['weight']
                sum_list.append(math.pow((float(a) / float(s)), 2))
                inv_part_dict[node] = sum(sum_list)

    return inv_part_dict


def out_ipr(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())

    inv_part_dict = {}
    for node in g.nodes():
        s = g.out_degree(node, weight='weight')
        successors = g.successors(node)
        if (len(successors) == 0 and s == 0):
            inv_part_dict[node] = 0
        else:
            sum_list = []
            for out_node in successors:
                a = g.edge[out_node][node]['weight']
                sum_list.append(math.pow((float(a) / float(s)), 2))
                inv_part_dict[node] = sum(sum_list)

    return inv_part_dict


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

    deg_sum = sum(g.in_degree().values())

    for i in g.nodes():
        if g.in_degree(i) > 0:
            entropy += ((g.in_degree(i) / float(deg_sum)) * (math.log(g.in_degree(i) / float(deg_sum))))

    entropy = -entropy / math.log(n)

    return entropy


def entropy_out_degree(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())
    n = g.number_of_nodes()

    entropy = 0

    deg_sum = sum(g.out_degree().values())

    for i in g.nodes():
        if g.out_degree(i) > 0:
            entropy += ((g.out_degree(i) / float(deg_sum)) * (math.log(g.out_degree(i) / float(deg_sum))))

    entropy = -entropy / math.log(n)

    return entropy


def entropy_degree(network):
    g = nx.read_weighted_edgelist(network)
    n = g.number_of_nodes()

    entropy = 0
    deg_sum = 0

    deg_sum = sum(g.degree().values())

    for i in g.nodes():
        if g.degree(i) > 0:
            entropy += ((g.degree(i) / float(deg_sum)) * (math.log(g.degree(i) / float(deg_sum))))

    entropy = -entropy / math.log(n)

    return entropy


def entropy_in_strenght(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())
    n = g.number_of_nodes()

    entropy = 0

    deg_sum = sum(g.in_degree(weight='weight').values())

    for i in g.nodes():
        if g.in_degree(i) > 0:
            entropy += ((g.in_degree(i, weight='weight') / float(deg_sum)) * (math.log(g.in_degree(i, weight='weight') / float(deg_sum))))

    entropy = -entropy / math.log(n)

    return entropy


def entropy_out_strenght(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())
    n = g.number_of_nodes()

    entropy = 0

    deg_sum = sum(g.out_degree(weight='weight').values())

    for i in g.nodes():
        if g.out_degree(i) > 0:
            entropy += ((g.out_degree(i, weight='weight') / float(deg_sum)) * (math.log(g.out_degree(i, weight='weight') / float(deg_sum))))

    entropy = -entropy / math.log(n)

    return entropy


def entropy_strenght(network):
    g = nx.read_weighted_edgelist(network)
    n = g.number_of_nodes()

    entropy = 0

    deg_sum = sum(g.degree(weight='weight').values())

    for i in g.nodes():
        if g.degree(i) > 0:
            entropy += ((g.degree(i, weight='weight') / float(deg_sum)) * (math.log(g.degree(i, weight='weight') / float(deg_sum))))

    entropy = -entropy / math.log(n)

    return entropy


def entropy_in_selectivity(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())
    n = g.number_of_nodes()

    entropy = 0
    sel_sum = 0
    selctivity_sequence = []

    for node in g.nodes():
        s = g.in_degree(node, weight='weight')
        k = g.in_degree(node, weight=None)
        if k > 0:
            selectivity = s / k
        else:
            selectivity = 0
        sel_sum += selectivity
        selctivity_sequence.append(selectivity)

    for selectivity in selctivity_sequence:
        if selectivity > 0:
            entropy += ((selectivity / float(sel_sum)) * (math.log(selectivity / float(sel_sum))))

    entropy = -entropy / math.log(n)

    return entropy


def entropy_out_selectivity(network):
    g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())
    n = g.number_of_nodes()

    entropy = 0
    sel_sum = 0
    selctivity_sequence = []

    for node in g.nodes():
        s = g.out_degree(node, weight='weight')
        k = g.out_degree(node, weight=None)
        if k > 0:
            selectivity = s / k
        else:
            selectivity = 0
        sel_sum += selectivity
        selctivity_sequence.append(selectivity)

    for selectivity in selctivity_sequence:
        if selectivity > 0:
            entropy += ((selectivity / float(sel_sum)) * (math.log(selectivity / float(sel_sum))))

    entropy = -entropy / math.log(n)

    return entropy


def entropy_selectivity(network):
    g = nx.read_weighted_edgelist(network)
    n = g.number_of_nodes()

    entropy = 0
    sel_sum = 0
    selctivity_sequence = []

    for node in g.nodes():
        s = g.degree(node, weight='weight')
        k = g.degree(node, weight=None)
        if k > 0:
            selectivity = s / k
        else:
            selectivity = 0
        sel_sum += selectivity
        selctivity_sequence.append(selectivity)

    for selectivity in selctivity_sequence:
        if selectivity > 0:
            entropy += ((selectivity / float(sel_sum)) * (math.log(selectivity / float(sel_sum))))

    entropy = -entropy / math.log(n)

    return entropy