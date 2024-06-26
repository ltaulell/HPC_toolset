#!/usr/bin/env python3
# coding: utf-8
#
# $Id: set-cpupower.py 4261 2023-12-11 15:08:57Z ltaulell $
# SPDX-License-Identifier: BSD-2-Clause
#

import argparse
import subprocess

from ClusterShell.NodeSet import NodeSet

"""
Apply CPU governor and min/max frequencies to NodeSet

TODO/FIXME:
* lack some hosts

* should use clusters.yml dictionary

* too much interactive -> cron-able

* VERY slow, should be //ized

"""


def apply_governor(freqs, host, debug=False):
    """
        apply chosen governor, with related freqs
    """
    cmd = ""
    match freqs['gov']:
        case "ondemand" | "performance":
            cmd = f"ssh root@{host} cpupower -c all frequency-set -g {freqs['gov']} --related --min {freqs['min']}MHz --max {freqs['max']}MHz"

        # case "performance":
        #    cmd = f"ssh root@{host} cpupower -c all frequency-set -g {freqs['gov']} --related --min {freqs['max']}MHz --max {freqs['max']}MHz"

        case "powersave":
            cmd = f"ssh root@{host} cpupower -c all frequency-set -g {freqs['gov']} --related --min {freqs['min']}MHz --max {freqs['min']}MHz"

    if debug:
        print(cmd)
        # print(f"subprocess.run({cmd}, capture_output=False, shell=True, check=False, text=False)")

    subprocess.run(cmd, capture_output=False, shell=True, check=False, text=False)


def get_args():
    """
        read parser and return args (as args namespace)
    """
    parser = argparse.ArgumentParser(description='Set CPU governor (with min/max frequencies)')
    parser.add_argument('-d', '--debug', action='store_true', help='toggle debug')
    parser.add_argument('-g', '--governor', nargs=1, type=str, choices=['powersave', 'ondemand', 'performance'], help='governor to apply (default: ondemand)', default=['ondemand'])
    parser.add_argument('nodes', type=str, help='host(s), nodeset syntax')

    return parser.parse_args()


def set_freqs(host, gouverneur):
    """
        set min/max frequencies according to CPU family
        return a dict{'min': int, 'max': int} or False
    """
    frequencies = {}
    match host:
        #
        # cluster E5
        #
        case host if host in NodeSet('c8220node[1-48,57-202],c6320node[201-212]'):
            # Intel E5-2670, Intel E5-2697Av4
            frequencies['min'] = "1200"
            frequencies['max'] = "2601"
            frequencies['gov'] = gouverneur

        case host if host in NodeSet('c8220node[49-56]'):
            # Intel E5-2650v2
            frequencies['min'] = "1200"
            frequencies['max'] = "2600"
            frequencies['gov'] = gouverneur

        case host if host in NodeSet('c6320node[1-24,101-124]'):
            # Intel E5-2667v4
            frequencies['min'] = "1200"
            frequencies['max'] = "3200"
            frequencies['gov'] = gouverneur
        #
        # cluster E5-GPU
        #
        case host if host in NodeSet('r730gpu[01-24]'):
            # Intel E5-2637v3
            frequencies['min'] = "1200"
            frequencies['max'] = "3500"
            frequencies['gov'] = gouverneur
        #
        # cluster Lake
        #
        case host if host in NodeSet('r740bigmem201,c6420node[061-168]'):
            # Intel 6226R CPU @ 2.90GHz
            frequencies['min'] = "1000"
            frequencies['max'] = "2900"
            frequencies['gov'] = gouverneur

        case host if host in NodeSet('c6420node[001-060,171-174]'):
            # Intel Gold 6142 2.60GHz
            frequencies['min'] = "1000"
            frequencies['max'] = "2600"
            frequencies['gov'] = gouverneur

        case host if host in NodeSet('6420node[201-204],xlr178node[001-106,109-110,119-122]'):
            # Intel Gold 5118 2.30GHz & Gold 5218 CPU @ 2.30GHz
            frequencies['min'] = "1000"
            frequencies['max'] = "2300"
            frequencies['gov'] = gouverneur

        case host if host in NodeSet('xlr170node[001-010,013-036,037-072]'):
            # Gold 6242 CPU @ 2.80GHz
            # flix ! change governor
            frequencies['min'] = "1000"
            frequencies['max'] = "2800"
            frequencies['gov'] = "ondemand"
        #
        # cluster Epyc
        #
        case host if host in NodeSet('c6525node[001-014]'):
            # AMD EPYC 7702
            frequencies['min'] = "1500"
            frequencies['max'] = "2000"
            frequencies['gov'] = gouverneur
        #
        # cluster Cascade
        #
        case host if host in NodeSet('s92node[41-52,79-80,85-86,103-108,113-120,127-144,193-196]'):
            # Intel Platinum 9242
            # flix ! change governor
            frequencies['min'] = "1000"
            frequencies['max'] = "2300"
            frequencies['gov'] = "ondemand"

        case host if host in NodeSet('s92node[01-40,53-78,81-84,87-90,109-112,121-126,145-150,163-192]'):
            # Intel Platinum 9242
            frequencies['min'] = "1000"
            frequencies['max'] = "2300"
            frequencies['gov'] = gouverneur

        # None of the above
        case _:
            print(f"Host not found in CPU tree: {host}")
            return False

    return frequencies


if __name__ == '__main__':
    """ """
    args = get_args()
    # debug
    if args.debug:
        debug = True
        print(args)
    else:
        debug = False

    nodes = NodeSet(args.nodes)
    if debug:
        print(f"{nodes}")

    for node in nodes:
        gov = args.governor[0]
        if debug:
            print(f"{gov}")

        freqs = set_freqs(node, gov)

        if freqs:
            if debug:
                print(f"{freqs}")

            apply_governor(freqs, node, debug=debug)
