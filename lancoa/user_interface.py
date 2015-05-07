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


class LaNCoA(object):

    def __dir__(self):
        commands = ['draw_plot', 'create']
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

    def create(self): Network()
    def draw_plot(self): Plot()


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
        commands = ['coocurrence_net', 'syntax_net']
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
        commands = ['rankplot', 'histogram']
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