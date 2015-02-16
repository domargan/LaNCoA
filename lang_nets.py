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


def cooccurrence_net(corpus, delimiter_list, d="directed",
                     w="weighted", window=1, lower="Yes"):
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

    nx.write_weighted_edgelist(g, corpus.rsplit(".", 1)[0] + "_coocurrence.edges")
    return g


def syntax_net(corpus, d="directed", w="weighted"):
    global g

    with open(corpus, "r", encoding='utf-8') as f:
        lines = f.readlines()
        lines.append("")

    sentences = []
    current = []
    for l in lines:
        cleaned = l.strip()
        if len(cleaned) == 0:
            sentences.append(current)
            current = []
        else:
            current.append(tuple(cleaned.split('\t')))

    lines_parsed = sentences

    def extract(sentence):
        reduced = [(0, 0, u'ROOT', u'Z')] + [(int(w[0]), int(w[6]), w[1], w[4]) for w in sentence]
        return reduced

    def remove_special(sentence):
        global parent_rest

        def first_special(sent):
            for word in sent:
                if word[2] == u'--' or word[2] == u'-' or word[2] == u'%':
                    continue
                if word[3] == u'Z':
                    return word[0], word[1]
            return ()

        def rename(name):
            if name == u'--' or name == u'-':
                return u'HYPHEN'
            elif name == u'%':
                return u'PERCENT'
            else:
                return name

        reduced = sentence
        to_replace = first_special(reduced)
        while to_replace:
            new_reduced = []
            is_first = True

            for word in reduced:
                if word[0] == to_replace[0]:
                    continue

                if word[1] == to_replace[0]:
                    if is_first:
                        is_first = False
                        parent = to_replace[1]
                        parent_rest = word[0]

                        if to_replace[0] == to_replace[1]:
                            parent = word[0]

                        new_reduced.append((word[0], parent, rename(word[2]), word[3]))
                    else:
                        new_reduced.append((word[0], parent_rest, rename(word[2]), word[3]))
                else:
                    new_reduced.append((word[0], word[1], rename(word[2]), word[3]))

            reduced = new_reduced
            to_replace = first_special(reduced)

        return reduced

    reduced_sentences = [remove_special(extract(sent)) for sent in lines_parsed]

    syntax_edges = dict()
    for sentence, i in zip(reduced_sentences, range(len(reduced_sentences))):
        name_map = dict()
        for word in sentence:
            name_map[word[0]] = word[2]

        for word in sentence:
            parent = word[1]
            current = word[0]
            edge = (name_map[parent], name_map[current])
            if edge in syntax_edges:
                syntax_edges[edge] += 1
            else:
                syntax_edges[edge] = 1

    syntax_list = [(k[0], k[1], v) for (k, v) in syntax_edges.items()]

    if d == "directed":
        g = nx.DiGraph()
    elif d == "undirected":
        g = nx.Graph()

    if w == "unweighted":
        g.add_edges_from(syntax_list)
    if w == "weighted":
        g.add_weighted_edges_from(syntax_list)

    nx.write_weighted_edgelist(g, corpus.rsplit(".", 1)[0] + "_syntax.edges")
    return g


def syllable_net(corpus, syllable_list, d="directed", w="weighted"):
    global g

    with open(corpus, "r", encoding='utf-8') as f:
        f_r = f.readlines()

    words = [line.split("\t") for line in f_r]

    with open(syllable_list, "r", encoding='utf-8') as f:
        f_r = f.readlines()

    syllables = [line.split() for line in f_r]

    if d == "directed":
        g = nx.DiGraph()
    elif d == "undirected":
        g = nx.Graph()

    syllable_edges = dict()

    for i in words:
        if len(i) > 1:
            for j in syllables:
                if i[1] == j[0]:
                    for l, r in zip(j[1].split("-")[:-1], j[1].split("-")[1:]):
                        edge = (l, r)
                        if edge in syllable_edges:
                            syllable_edges[edge] += 1
                        else:
                            syllable_edges[edge] = 1
                else:
                    g.add_node(i[1])

    edge_list = [(k[0], k[1], v) for (k, v) in syllable_edges.items()]

    if w == "unweighted":
        g.add_edges_from(edge_list)
    if w == "weighted":
        g.add_weighted_edges_from(edge_list)

    nx.write_weighted_edgelist(g, corpus.rsplit(".", 1)[0] + "_syllable.edges")
    return g


def grapheme_net(syllable_network, d="directed", w="weighted"):
    global syllable_net

    if d == "directed":
        syllable_net = nx.read_weighted_edgelist(syllable_network, create_using=nx.DiGraph())
        g = nx.DiGraph()
    elif d == "undirected":
        syllable_net = nx.read_weighted_edgelist(syllable_network)
        g = nx.Graph()

    for node in syllable_net.nodes():
        graphemes = list(node)
        for i, gr in enumerate(graphemes):
            if i > 0:
                if w == "weighted":
                    if g.has_edge(graphemes[i - 1], graphemes[i]):
                        g[graphemes[i - 1]][graphemes[i]]['weight'] += 1
                    else:
                        g.add_edge(graphemes[i - 1], graphemes[i], weight=1)
                elif w == "unweighted":
                    g.add_edge(graphemes[i - 1], graphemes[i])

    nx.write_weighted_edgelist(g, syllable_network.rsplit(".", 1)[0] + "_grapheme.edges")
    return g