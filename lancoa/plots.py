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
import matplotlib.pyplot as plt
import matplotlib
from collections import OrderedDict


def in_selectivity_rank_plot(network1, network2=None, network3=None, network4=None, network5=None, network6=None):
    networks = OrderedDict(sorted(locals().items()))

    xlabel = "rank"
    ylabel = "in_selectivity"
    figname = "in_selectivity_rank.png"

    for v in networks.itervalues():
        if v != None:
            g = nx.read_weighted_edgelist(v, create_using=nx.DiGraph())

            selectivity_dict = {}
            for node in g.nodes():
                s = g.in_degree(node, weight='weight')
                k = g.in_degree(node, weight=None)
                if k > 0:
                    selectivity = s / k
                    selectivity_dict[node] = selectivity
                else:
                    selectivity_dict[node] = 0
            selectivity = selectivity_dict.values()
            selectivity_sequence = sorted(selectivity,reverse=True)
            plt.loglog(selectivity_sequence, 'b-', color='blue', lw=3, alpha=0.7, marker='o', label=str(k))
            plt.savefig(figname)