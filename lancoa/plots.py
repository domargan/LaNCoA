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

import measures
import matplotlib.pyplot as plt
import networkx as nx

__author__ = "Domagoj Margan"
__email__ = "margan.domagoj@gmail.com"
__copyright__ = "Copyright 2015, Domagoj Margan"
__license__ = "GPL"


def selectivity_rank_plot(name, network1, network2=None, network3=None,
                          network4=None, network5=None, network6=None,
                          d="undirected"):
    figname = str(name)

    colors = ["blue", "red", "green", "cyan", "magenta", "yellow"]
    color_idx = 0
    markers = ["o", "v", "^", "s", "*", "p"]
    marker_idx = 0

    networks = [network1, network2, network3, network4, network5, network6]

    for net in networks:
        if net != None:
            if d == "in":
                selectivity_dict = measures.in_selectivity(net)
            elif d == "out":
                selectivity_dict = measures.out_selectivity(net)
            elif d == "undirected":
                selectivity_dict = measures.selectivity(net)

            selectivity = selectivity_dict.values()
            selectivity_sequence = sorted(selectivity, reverse=True)

            plt.loglog(selectivity_sequence, 'b-', color=colors[color_idx],
                       lw=3, alpha=0.7, marker=markers[marker_idx],
                       label=net.rsplit(".", 1)[0])
            plt.savefig(figname)

            color_idx += 1
            marker_idx += 1

            plt.xlabel("rank")
            if d == "in":
                plt.ylabel("in-selectivity")
            elif d == "out":
                plt.ylabel("out-selectivity")
            elif d == "undirected":
                plt.ylabel("selectivity")

            plt.legend(loc=1, shadow=True)
            plt.savefig(figname)

    plt.clf()


def degree_rank_plot(name, network1, network2=None, network3=None,
                          network4=None, network5=None, network6=None,
                          d="undirected"):
    figname = str(name)

    colors = ["blue", "red", "green", "cyan", "magenta", "yellow"]
    color_idx = 0
    markers = ["o", "v", "^", "s", "*", "p"]
    marker_idx = 0

    networks = [network1, network2, network3, network4, network5, network6]

    for net in networks:
        if net != None:
            if d == "in":
                g = nx.read_weighted_edgelist(net, create_using=nx.DiGraph())
                degree_dict = g.in_degree()
            elif d == "out":
                g = nx.read_weighted_edgelist(net, create_using=nx.DiGraph())
                degree_dict = g.out_degree()
            elif d == "undirected":
                g = nx.read_weighted_edgelist(net)
                degree_dict = g.degree()

            degree = degree_dict.values()
            degree_sequence = sorted(degree, reverse=True)

            plt.loglog(degree_sequence, 'b-', color=colors[color_idx],
                       lw=3, alpha=0.7, marker=markers[marker_idx],
                       label=net.rsplit(".", 1)[0])
            plt.savefig(figname)

            color_idx += 1
            marker_idx += 1

            plt.xlabel("rank")
            if d == "in":
                plt.ylabel("in-degree")
            elif d == "out":
                plt.ylabel("out-degree")
            elif d == "undirected":
                plt.ylabel("degree")

            plt.legend(loc=1, shadow=True)
            plt.savefig(figname)

    plt.clf()


def strengtt_rank_plot(name, network1, network2=None, network3=None,
                          network4=None, network5=None, network6=None,
                          d="undirected"):
    figname = str(name)

    colors = ["blue", "red", "green", "cyan", "magenta", "yellow"]
    color_idx = 0
    markers = ["o", "v", "^", "s", "*", "p"]
    marker_idx = 0

    networks = [network1, network2, network3, network4, network5, network6]

    for net in networks:
        if net != None:
            if d == "in":
                g = nx.read_weighted_edgelist(net, create_using=nx.DiGraph())
                strength_dict = g.in_degree(weight='weight')
            elif d == "out":
                g = nx.read_weighted_edgelist(net, create_using=nx.DiGraph())
                strength_dict = g.out_degree(weight='weight')
            elif d == "undirected":
                g = nx.read_weighted_edgelist(net)
                strength_dict = g.degree(weight='weight')

            strength = strength_dict.values()
            strength_sequence = sorted(strength, reverse=True)

            plt.loglog(strength_sequence, 'b-', color=colors[color_idx],
                       lw=3, alpha=0.7, marker=markers[marker_idx],
                       label=net.rsplit(".", 1)[0])
            plt.savefig(figname)

            color_idx += 1
            marker_idx += 1

            plt.xlabel("rank")
            if d == "in":
                plt.ylabel("in-strength")
            elif d == "out":
                plt.ylabel("out-strength")
            elif d == "undirected":
                plt.ylabel("strength")

            plt.legend(loc=1, shadow=True)
            plt.savefig(figname)

    plt.clf()