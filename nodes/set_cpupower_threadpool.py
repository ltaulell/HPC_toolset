#!/usr/bin/env python3
# coding: utf-8
#
# $Id: set_cpupower_threadpool+ref.py 4624 2024-07-02 14:45:12Z ltaulell $
# SPDX-License-Identifier: BSD-2-Clause
#
"""
https://www.pythontutorial.net/python-concurrency/python-threadpoolexecutor/

TODO/FIXME:


"""

import argparse
import subprocess
import yaml
import sys

from ClusterShell.NodeSet import NodeSet
from concurrent.futures import ThreadPoolExecutor


nodes_ok = NodeSet()
nodes_ko = NodeSet()
list_freqs = []
debug = False
KEYFILE = '-o "IdentitiesOnly=yes" -i /path/to/keyfile'
fanout = 1
timeout = 10

# frequencies changes do not apply on these:
blacklist = NodeSet()
visu = NodeSet("r740flix[1-4],r740gpu[06-09],r740visu,r740cral,r640cral")
premium = NodeSet("s92node[61-78],xlr170node[001-010,013-036,037-060]")


def apply_governor(freqs):
    """
        apply chosen governor, with related freqs
    """
    cmd = ""
    match freqs['gov']:
        case "ondemand" | "performance":
            cmd = f"ssh {KEYFILE} root@{freqs['host']} cpupower -c all frequency-set -g {freqs['gov']} --related --min {freqs['min']}MHz --max {freqs['max']}MHz"

        case "powersave":
            cmd = f"ssh {KEYFILE} root@{freqs['host']} cpupower -c all frequency-set -g {freqs['gov']} --related --min {freqs['min']}MHz --max {freqs['min']}MHz"

    if debug:
        print(cmd)
        try:
            subprocess.run(cmd, capture_output=False, shell=True, check=True, text=True, timeout=timeout)
        except subprocess.CalledProcessError as err:
            print(f"problem with {freqs['host']}")
            print(err)
            nodes_ko.add(freqs['host'])
            pass
        else:
            nodes_ok.add(freqs['host'])
    else:
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, shell=True, check=True, text=True, timeout=timeout)
        except subprocess.CalledProcessError:
            print(f"problem with {freqs['host']}")
            nodes_ko.add(freqs['host'])
            pass
        else:
            nodes_ok.add(freqs['host'])


def get_args():
    """
        read parser and return args (as args namespace)
    """
    parser = argparse.ArgumentParser(description='Set CPU governor (with min/max frequencies)')
    parser.add_argument('-d', '--debug', action='store_true', help='toggle debug')
    parser.add_argument('-k', '--keyfile', action='store_true', help='activate keyfile (default=False)')
    parser.add_argument('-g', '--governor', nargs=1, type=str, choices=['powersave', 'ondemand', 'performance'], help='governor to apply (default: ondemand)', default=['ondemand'])
    parser.add_argument("-f", "--fanout", action="store", default="128", help="Fanout window size (default 128)", type=int)
    parser.add_argument("-t", "--timeout", action="store", default="10", help="Timeout in seconds (default 10)", type=float)
    parser.add_argument('-r', '--repository', type=str, help='repository file (default: clusters.yml)', default=['clusters.yml'])
    parser.add_argument('nodes', type=str, help='host(s), nodeset syntax')

    return parser.parse_args()


def load_yaml_file(yamlfile):
    """
    load data from a yaml file, using safe_load, return a dict{}.

    yamlfile is mandatory. Throw yaml errors, if any.

    import sys
    import yaml

    """
    try:
        with open(yamlfile, 'r') as fichier:
            contenu = yaml.safe_load(fichier)
            return contenu
    except IOError:
        print("Unable to open file: {}".format(fichier.name))
        sys.exit(1)
    except yaml.YAMLError as erreur:
        if hasattr(erreur, 'problem_mark'):
            mark = erreur.problem_mark
            # print("YAML error position: (%s:%s) in" % (mark.line + 1, mark.column + 1), fichier.name)
            print('YAML error position: ({}:{}) in {}'.format(mark.line + 1, mark.column + 1, fichier.name))
        sys.exit(1)


def get_nodes_freq(node, gouverneur, debug=False):
    """
        get info for node, from cluster repository

        return a dict{'host', str, 'min': int, 'max': int, 'gov': str}
        or return False
    """

    frequencies = {}
    global blacklist

    if node in blacklist:
        if debug:
            print(f"{node} in blacklist")
        return False
    else:
        for cluster in NODESREF.keys():
            for group in NODESREF[cluster].keys():
                nodeset = NodeSet(group)
                if node in nodeset:
                    if debug:
                        print(f"{node} in {nodeset}, {NODESREF[cluster][group]['groupAltName']}")
                    frequencies['host'] = node
                    frequencies['min'] = NODESREF[cluster][group]['nodeCPUFreqMin']  # nodeCPUFreqMin
                    frequencies['max'] = NODESREF[cluster][group]['nodeCPUFreqMax']  # nodeCPUFreqMax
                    frequencies['gov'] = gouverneur

                    return frequencies


if __name__ == '__main__':
    """ """
    args = get_args()
    # debug
    if args.debug:
        debug = True
        print(args)

    if args.repository:
        REFERENTIEL = args.repository[0]

    NODESREF = load_yaml_file(REFERENTIEL)

    blacklist.add(visu)
    blacklist.add(premium)

    fanout = args.fanout
    timeout = args.timeout

    if not args.keyfile:
        KEYFILE = ''

    nodes = NodeSet(args.nodes)
    if debug:
        print(f"{nodes}")

    for node in nodes:
        gov = args.governor[0]
        if debug:
            print(f"{gov}")

        result = get_nodes_freq(node, gov, debug)
        if result:
            list_freqs.append(result)
        else:
            nodes_ko.add(node)

    if list_freqs:
        if debug:
            print(f"{list_freqs}")

        with ThreadPoolExecutor(max_workers=fanout) as executor:
            results = executor.map(apply_governor, list_freqs)

    print(f"Nodes OK: {nodes_ok}")
    print(f"Nodes KO: {nodes_ko}")
