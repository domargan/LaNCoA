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