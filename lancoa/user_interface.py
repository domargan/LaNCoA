#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 Tanja Miličić <tanyamilicic@gmail.com>

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

__author__ = "Tanja Miličić"
__email__ = "tanyamilicic@gmail.com"
__copyright__ = "Copyright 2015, Tanja Miličić"
__license__ = "GPL"


import argparse
import sys
import plots
import lang_nets
import text_corpora
import measures


class LaNCoA(object):

    def __dir__(self):
        commands = ['draw_plot', 'create', 'corpora', 'calculate']
        return commands

    def __init__(self):
        commands = '\t'.join(dir(self))
        parser = argparse.ArgumentParser(
            add_help=False,
            prog='lancoa.py',
            usage='''%(prog)s [COMMAND] [SUBCOMMAND] [ARGS]

            Available commands are:
            ''' + commands,
            description='',
        )
        parser.add_argument('command', help="")
        args = parser.parse_args(sys.argv[1:2])
        if hasattr(self, args.command):
            getattr(self, args.command)()
        else:
            print 'Unrecognized command'
            parser.print_help()
            exit(1)

    def corpora(self): Corpora()
    def create(self): Network()
    def calculate(self): Measure()
    def draw_plot(self): Plot()


class Corpora(object):

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('corpora_file')

    def __init__(self):
        commands = ' '.join(dir(self))
        parser = argparse.ArgumentParser(
            add_help=False,
            usage='''corpora [COMMAND] [ARGS]

            Available corpora manipulation commands are:
            ''' + commands
        )
        parser.add_argument('command', help='')
        args = parser.parse_args(sys.argv[2:3])
        if hasattr(self, args.command):
            getattr(self, args.command)()
        else:
            print 'Unrecognized command'
            parser.print_help()
            exit(1)

    def __dir__(self):
        commands = ['remove_stopwords', 'lemmatize',
                    'clean_corpus', 'shuffle_corpus']
        return commands

    def remove_stopwords(self):
        parser = argparse.ArgumentParser(prog='remove_stopwords',
                                         parents=[Corpora.parent_parser])
        parser.add_argument('delimiters')
        parser.add_argument('stopwords_file')
        args = parser.parse_args(sys.argv[3:])
        text_corpora.remove_stopwords(args.corpora_file, args.delimiters, args.stopwords_file)

    def lemmatize(self):
        parser = argparse.ArgumentParser(prog='lemmatize',
                                         parents=[Corpora.parent_parser])
        parser.add_argument('delimiters')
        parser.add_argument('lemmas_file')
        parser.add_argument('lemma_splitter')
        args = parser.parse_args(sys.argv[3:])
        text_corpora.lemmatize(args.corpus_file, args.delimiters,
                               args.lemmas_file, args.lemma_splitter)

    def clean_corpus(self):
        parser = argparse.ArgumentParser(prog='clean_corpus',
                                         parents=[Corpora.parent_parser])
        parser.add_argument('preserve_list', default='None', nargs='+')
        parser.add_argument('--nfdk', default='No', choices=['Yes', 'No'])
        parser.add_argument('--split', default='No', choices=['Yes', 'No'])
        parser.add_argument('--replace', default='')
        args = parser.parse_args(sys.argv[3:])
        text_corpora.clean_corpus(args.corpus_file, args.preserve_list,
                                  args.nfkd, args.split, args.replace)

    def shuffle_corpus(self):
        parser = argparse.ArgumentParser(prog='shuffle_corpus',
                                         parents=[Corpora.parent_parser])
        parser.add_argument('delimiters')
        parser.add_argument('node')
        parser.add_argument('end_sign')
        args = parser.parse_args(sys.argv[3:])
        text_corpora.shuffle_corpus(args.corpus_file, args.delimiters,
                                    args.node, args.end_sign)


class Network(object):

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-d', default='directed', choices=['directed', 'undirected'])
    parent_parser.add_argument('-w', default='weighted', choices=['weighted', 'unweighted'])

    def __init__(self):
        commands = ' '.join(dir(self))
        parser = argparse.ArgumentParser(
            add_help=False,
            usage='''create [NETWORK] [ARGS]

            Available networks are: ''' + commands
        )
        parser.add_argument('command', help="")
        args = parser.parse_args(sys.argv[2:3])
        if hasattr(self, args.command):
            getattr(self, args.command)()
        else:
            print 'Unrecognized command'
            parser.print_help()
            exit(1)

    def __dir__(self):
        commands = ['coocurrence_net', 'syntax_net', 'syllable_net',
                    'grapheme_net', 'wordlist_subnet', 'ego_word_subnet']
        return commands

    def coocurrence_net(self):
        parser = argparse.ArgumentParser(prog='coocurrence_net',
                                         parents=[Network.parent_parser])
        parser.add_argument('corpus_file')
        parser.add_argument('delimiters', nargs='+')
        parser.add_argument('--window', type=int, default=1)
        parser.add_argument('--lower', default='Yes', choices=['Yes', 'No'])
        args = parser.parse_args(sys.argv[3:])
        lang_nets.cooccurrence_net(args.corpus_file, list(args.delimiters),
                                   args.d, args.w, args.window, args.lower)

    def syntax_net(self):
        parser = argparse.ArgumentParser(prog='syntax_net',
                                         parents=[Network.parent_parser])
        parser.add_argument('corpus_file')
        args = parser.parse_args(sys.argv[3:])
        lang_nets.syntax_net(args.corpus_file, args.d, args.w)

    def syllable_net(self):
        parser = argparse.ArgumentParser(prog='syllable_net',
                                         parents=[Network.parent_parser])
        parser.add_argument('corpus_file')
        parser.add_argument('syllable_list')
        args = parser.parse_args(sys.argv[3:])
        lang_nets.syllable_net(args.corpus_file, args.syllable_list, args.d, args.w)

    def grapheme_net(self):
        parser = argparse.ArgumentParser(prog='grapheme_net',
                                         parents=[Network.parent_parser])
        parser.add_argument('syllable_network')
        args = parser.parse_args(sys.argv[3:])
        lang_nets.grapheme_net(args.syllable_network, args.d, args.w)

    def wordlist_subnet(self):
        parser = argparse.ArgumentParser(prog='wordlist_subnet',
                                         parents=[Network.parent_parser])
        parser.add_argument('word_network')
        parser.add_argument('word')
        parser.add_argument('words_file')
        args = parser.parse_args(sys.argv[3:])
        lang_nets.wordlist_subnet(args.word_network, args.word,
                                  args.words_file, args.d, args.w)

    def ego_word_subnet(self):
        parser = argparse.ArgumentParser(prog='ego_word_subnet',
                                         parents=[Network.parent_parser])
        parser.add_argument('word_network')
        parser.add_argument('word')
        parser.add_argument('neighborhood', default='all',
                            choices=['successors', 'predecessors', 'all'])
        parser.add_argument('--radius', type=int, default=1)
        args = parser.parse_args(sys.argv[3:])
        lang_nets.ego_word_subnet(args.word_network, args.word, args.radius,
                                  args.d, args.w, args.neighborhood)


class Measure(object):

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('network')

    def __init__(self):
        parser = argparse.ArgumentParser(
            add_help=False,
            usage='''calculate [MEASURE] [ARGS]'''
        )
        parser.add_argument('command')
        args = parser.parse_args(sys.argv[2:3])
        if hasattr(self, args.command):
            getattr(self, args.command)()
        else:
            print 'Unrecognized command'
            parser.print_help()
            exit(1)

    def __dir__(self):
        commands = []
        return commands

    def reciprocity(self):
        parser = argparse.ArgumentParser(prog='reciprocity',
                                         parents=[Measure.parent_parser])
        args = parser.parse_args(sys.argv[3:])
        print measures.reciprocity(args.network)


class Plot(object):

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('name')
    parent_parser.add_argument('-d', default='in', choices=['in', 'out', 'undirected'])
    parent_parser.add_argument('-m', default='degree', choices=['degree', 'selectivity', 'strength'])

    def __init__(self):
        commands = ' '.join(dir(self))
        parser = argparse.ArgumentParser(
            add_help=False,
            usage='''draw_plot [PLOT] [ARGS]

            Available plots are: ''' + commands
        )
        parser.add_argument('command', help="")
        args = parser.parse_args(sys.argv[2:3])
        if hasattr(self, args.command):
            getattr(self, args.command)()
        else:
            print 'Unrecognized command'
            parser.print_help()
            exit(1)

    def __dir__(self):
        commands = ['rankplot', 'histogram', 'scatterplot']
        return commands

    def rankplot(self):
        parser = argparse.ArgumentParser(prog='rankplot', parents=[Plot.parent_parser])
        parser.add_argument('networks', nargs='+')
        args = parser.parse_args(sys.argv[3:])
        plots.draw_rank_plot(args.name, args.networks, args.d, args.m)

    def histogram(self):
        parser = argparse.ArgumentParser(prog='histogram', parents=[Plot.parent_parser])
        parser.add_argument('network')
        args = parser.parse_args(sys.argv[3:])
        plots.draw_histogram(args.name, args.network, args.d, args.m)

    def scatterplot(self):
        parser = argparse.ArgumentParser(prog='scatterplot')
        parser.add_argument('name')
        parser.add_argument('networks', nargs='+')
        parser.add_argument('-d', default='in', choices=['in', 'out', 'undirected'])
        parser.add_argument('-y', default='degree', choices=['degree', 'selectivity', 'strength'])
        parser.add_argument('-x', default='strength', choices=['degree', 'selectivity', 'strength'])
        args = parser.parse_args(sys.argv[3:])
        plots.draw_scatterplot(args.name, args.networks, args.d, args.x, args.y)