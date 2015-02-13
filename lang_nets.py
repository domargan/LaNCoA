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

from codecs import open

__author__ = "Domagoj Margan"
__email__ = "margan.domagoj@gmail.com"
__copyright__ = "Copyright 2015, Domagoj Margan"
__license__ = "GPL"


def cooccurrence_net(corpus, delimiter_list, d="directed",
                     w="weighted", window=1, lower="Yes"):
    import networkx as nx
    global c_list, g

    with open(corpus, "r", encoding='utf-8') as f:
        if lower == "Yes":
            c_list = f.read().lower().split()
        elif lower == "No":
            c_list = f.read().split()

    if d == "directed":
        g = nx.DiGraph()
    elif d == "undirected":
        g = nx.Graph()

    delimiters = ''.join(delimiter_list)

    if w == "unweighted":
        for i, word in enumerate(c_list):
            for j in range(1, window + 1):
                if i - j >= 0 and c_list[i - j][-1] not in delimiter_list:
                    g.add_edge(c_list[i - j], c_list[i].strip(delimiters))
                else:
                    break
    elif w == "weighted":
        for i, word in enumerate(c_list):
            for j in range(1, window + 1):
                if i - j >= 0 and c_list[i - j][-1] not in delimiter_list:
                    if g.has_edge(c_list[i - j], c_list[i].strip(delimiters)):
                        g[c_list[i - j]][c_list[i].strip(delimiters)]['weight'] += 1
                    else:
                        g.add_edge(c_list[i - j], c_list[i].strip(delimiters), weight=1)
                else:
                    break

    nx.write_weighted_edgelist(g, corpus.rsplit(".", 1)[0] + ".edges")
    return g