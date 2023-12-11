#!/usr/bin/env python3
# coding: utf-8
#
# $Id: set-cpupower.py 4261 2023-12-11 15:08:57Z ltaulell $
# SPDX-License-Identifier: BSD-2-Clause
#

import argparse

from ClusterShell.NodeSet import NodeSet

"""

NOT DONE YET!!




si @comp et @visu doivent être en 'powersave' :
        # cluster X5
        case hosts if hosts in NodeSet('x5570comp[1-2]'):
            # Intel X5570
            frequencies['min'] = "1600"
            frequencies['max'] = "2930"

"""

GOVERNORS="powersave ondemand performance"


def apply_governor(governor, freqs, debug=False):
    """
        apply chosen governor, with freqs, if needed
    """
    match governor:
        case "ondemand":
            if debug:
                print("cpupower -c all frequency-set -g ondemand")
            # cpupower -c all frequency-set -g ondemand
            pass
        case "performance":
            if debug:
                print("cpupower -c all frequency-set -g performance")
            # cpupower -c all frequency-set -g performance
            pass
        case "powersave":
            if debug:
                print(f"cpupower -c all frequency-set --related --min {freqs['min']}Mhz --max {freqs['min']}Mhz")
            # cmd = f"cpupower -c all frequency-set --related --min {freqs['min']}Mhz --max {freqs['min']}Mhz"
            pass


def get_args():
    """
        read parser and return args (as args namespace)
    """
    parser = argparse.ArgumentParser(description='Set cpupower governor (and cpu min/max frequencies)')
    parser.add_argument('-d', '--debug', action='store_true', help='toggle debug')
    parser.add_argument('-g', '--governor', nargs=1, type=str, choices=['powersave', 'ondemand', 'performance'], help='governor to apply (default: ondemand)', default='ondemand')
    parser.add_argument('nodes', type=str, help='host(s), nodeset syntax')

    return parser.parse_args()


def set_freqs(hosts):
    """
        set min/max frequencies according to CPU family
        return a dict{'min': int, 'max': int}
    """
    frequencies = {}
    match hosts:
        #
        # cluster E5
        #
        case hosts if hosts in NodeSet('c8220node[1-48,57-202],c6320node[201-212]'):
            # Intel E5-2670, Intel E5-2697Av4
            frequencies['min'] = "1200"
            frequencies['max'] = "2601"
        case hosts if hosts in NodeSet('c8220node[49-56]'):
            # Intel E5-2650v2
            frequencies['min'] = "1200"
            frequencies['max'] = "2600"
        case hosts if hosts in NodeSet('c6320node[1-24,101-124]'):
            # Intel E5-2667v4
            frequencies['min'] = "1200"
            frequencies['max'] = "3200"
        #
        # cluster E5-GPU
        #
        case hosts if hosts in NodeSet('r730gpu[01-24]'):
            # Intel E5-2637v3
            frequencies['min'] = "1200"
            frequencies['max'] = "3500"
        #
        # cluster Lake
        #
        case hosts if hosts in NodeSet('r740bigmem201,c6420node[061-168]'):
            # Intel 6226R CPU @ 2.90GHz
            frequencies['min'] = "1000"
            frequencies['max'] = "2900"
        case hosts if hosts in NodeSet('c6420node[001-060,171-174]'):
            # Intel Gold 6142 2.60GHz
            frequencies['min'] = "1000"
            frequencies['max'] = "2600"
        case hosts if hosts in NodeSet('6420node[201-204],xlr178node[001-106,109-110,119-122]'):
            # Intel Gold 5118 2.30GHz & Gold 5218 CPU @ 2.30GHz
            frequencies['min'] = "1000"
            frequencies['max'] = "2300"
        case hosts if hosts in NodeSet('xlr170node[001-010,013-036,037-072]'):
            # Gold 6242 CPU @ 2.80GHz
            # flix ! no min
            # frequencies['min'] = "1000"
            frequencies['min'] = "2800"
            frequencies['max'] = "2800"
        #
        # cluster Epyc
        #
        case hosts if hosts in NodeSet('c6525node[001-014]'):
            # AMD EPYC 7702
            frequencies['min'] = "1500"
            frequencies['max'] = "2000"
        #
        # cluster Cascade
        #
        case hosts if hosts in NodeSet('s92node[41-52,79-80,85-86,103-108,113-120,127-144,193-196]'):
            # Intel Platinum 9242
            # flix ! no min
            frequencies['min'] = "2300"
            frequencies['max'] = "2300"
        case hosts if hosts in NodeSet('s92node[02-40,53-78,81-84,87-90,109-112,121-126,145-150,163-192]'):
            # Intel Platinum 9242
            frequencies['min'] = "1000"
            frequencies['max'] = "2300"

        # None of the above
        case _:
            raise ValueError(f"Host not found in CPU tree: {hosts}")

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

    freqs = set_freqs(nodes)
    if debug:
        print(f"{freqs}")

    gov = args.governor[0]
    if gov in GOVERNORS:
        apply_governor(gov, freqs, debug=debug)