#!/usr/bin/env python3
# coding: utf-8

# $Id: test_referentiel.py 4481 2024-04-26 07:11:35Z ltaulell $
# SPDX-License-Identifier: CECILL-B

"""

    http://pyyaml.org/wiki/PyYAMLDocumentation

"""

import argparse
import yaml
import sys

from pprint import pprint
from ClusterShell.NodeSet import NodeSet


DICTFILE = "clusters.yml"


def get_args():
    """
        read parser and return args (as args namespace)
    """
    parser = argparse.ArgumentParser(description="test lecture yaml")
    parser.add_argument("-d", "--debug", action="store_true", help="toggle debug (default: no)")
    parser.add_argument('-f', '--refile', type=str, help='referential file', default=None)
    parser.add_argument('-n', '--node', type=str, help='node (or nodeset group)', default=None)
    # please see Common.py for argparse examples
    args = parser.parse_args()

    return args


def load_yaml_file(yamlfile):
    """ load data from a yaml file, using safe_load, return a dict{}.

    yamlfile is mandatory. Throw yaml errors, if any.

    import sys
    import yaml

    """
    try:
        with open(yamlfile, 'r') as fichier:
            contenu = yaml.safe_load(fichier)
            return(contenu)
    except IOError:
        print("Unable to open file: {}".format(fichier.name))
        sys.exit(1)
    except yaml.YAMLError as erreur:
        if hasattr(erreur, 'problem_mark'):
            mark = erreur.problem_mark
            # print("YAML error position: (%s:%s) in" % (mark.line + 1, mark.column + 1), fichier.name)
            print('YAML error position: ({}:{}) in {}'.format(mark.line + 1, mark.column + 1, fichier.name))
        sys.exit(1)


if __name__ == '__main__':
    """ """
    args = get_args()
    if args.debug:
        debug = True
    else:
        debug = False

    if args.refile:
        DICTFILE = args.refile

    if args.node:
        nodes = NodeSet(args.node)
    else:
        nodes = None

    nodesdict = load_yaml_file(DICTFILE)
    # pprint(nodesdict)
    for cluster in nodesdict.keys():
        for group in nodesdict[cluster].keys():
            nodeset = NodeSet(group)
            if debug:
                print(f"nodeset: {nodeset}")
            if nodes:
                if debug:
                    print(f"nodes: {nodes}")
                for node in nodes:
                    if node in nodeset:
                        print(f"{nodeset}, {nodesdict[cluster][group]['groupAltName']}")
                        print(f"scratch: {nodesdict[cluster][group]['nodeScratchNumber']}")
                        print(f"freqmin: {nodesdict[cluster][group]['nodeCPUFreqMin']}")
                        print(f"freqmax: {nodesdict[cluster][group]['nodeCPUFreqMax']}")

