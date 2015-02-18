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
import networkx as nx

__author__ = "Domagoj Margan"
__email__ = "margan.domagoj@gmail.com"
__copyright__ = "Copyright 2015, Domagoj Margan"
__license__ = "GPL"


def hubs(network, n, d="directed"):
    n = int(n)

    if d == "directed":
        g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())
        if g.number_of_nodes() < n:
            n = int(g.number_of_nodes())

        degree_list_in = [node for node in g.in_degree().iteritems()]
        degree_list_in.sort(key=lambda x: x[1])
        degree_list_in.reverse()
        degree_list_out = [node for node in g.out_degree().iteritems()]
        degree_list_out.sort(key=lambda x: x[1])
        degree_list_out.reverse()

        with open(network.rsplit(".", 1)[0] + "_hubs_in.txt", "w",
                  encoding="utf-8") as write_f_in:
            for i, value in enumerate(degree_list_in):
                if i < n:
                    write_f_in.write(str(value[0]) + "\t\tIn-degree: " + str(value[1]) + "\n")
                else:
                    break

        with open(network.rsplit(".", 1)[0] + "_hubs_out.txt", "w",
                  encoding="utf-8") as write_f_out:
            for i, value in enumerate(degree_list_out):
                if i < n:
                    write_f_out.write(str(value[0]) + "\t\tOut-degree: " + str(value[1]) + "\n")
                else:
                    break

    elif d == "undirected":
        g = nx.read_weighted_edgelist(network)
        if g.number_of_nodes() < n:
            n = int(g.number_of_nodes())

        degree_list = [node for node in g.degree().iteritems()]
        degree_list.sort(key=lambda x: x[1])
        degree_list.reverse()

        with open(network.rsplit(".", 1)[0] + "_hubs.txt", "w",
                  encoding="utf-8") as write_f:
            for i, value in enumerate(degree_list):
                if i < n:
                    write_f.write(str(value[0]) + "\t\tDegree: " + str(value[1]) + "\n")
                else:
                    break


def weightiest_edges(network, n=20, d="directed"):
    if d == "directed":
        g = nx.read_weighted_edgelist(network, create_using=nx.DiGraph())
    elif d == "undirected":
        g = nx.read_weighted_edgelist(network)

    if g.number_of_edges() < n:
        n = g.number_of_edges()

    weight_dict = {(u, v): i['weight'] for (u, v, i) in g.edges(data=True)}
    weight_list = [edge for edge in weight_dict.iteritems()]
    weight_list.sort(key=lambda x: x[1])
    weight_list.reverse()

    with open(network.rsplit(".", 1)[0] + "_weightiest_edges.txt", "w",
              encoding="utf-8") as write_f:
        for i, value in enumerate(weight_list):
            if i < n:
                write_f.write(str(value[0][0]) + "\t\t: " +
                              str(value[0][1]) + "\t\t" + str(value[1]) + "\n")
            else:
                break