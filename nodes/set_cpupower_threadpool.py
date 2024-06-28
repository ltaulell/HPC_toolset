#!/usr/bin/env python3
# coding: utf-8
#
# $Id: set_cpupower_threadpool.py 4599 2024-06-19 15:06:57Z ltaulell $
# SPDX-License-Identifier: BSD-2-Clause
#
"""
<<<<<<< HEAD
TODO/FIXME:

- use ThreadPoolExecutor() to //-ize

- handle timeout

- handle OK/NOOK (via nodesets?)

https://www.pythontutorial.net/python-concurrency/python-threadpoolexecutor/
=======
//ized version of set-cpupower.py using ThreadPoolExecutor

from 33mn using sequential set-cpupower.py to 5mn for 658 nodes.

https://www.pythontutorial.net/python-concurrency/python-threadpoolexecutor/

TODO/FIXME:

* should use clusters.yml dictionary
>>>>>>> cfa0ea7958a516dc7b07be0b8a7abe2e93eb57a9

"""

import argparse
import subprocess

from ClusterShell.NodeSet import NodeSet
from concurrent.futures import ThreadPoolExecutor


nodes_ok = NodeSet()
nodes_ko = NodeSet()
list_freqs = []
debug = False
<<<<<<< HEAD
=======
USER = 'root'
>>>>>>> cfa0ea7958a516dc7b07be0b8a7abe2e93eb57a9
KEYFILE = ''
fanout = 1
timeout = 10


def apply_governor(freqs):
    """
        apply chosen governor, with related freqs
    """
    cmd = ""
    match freqs['gov']:
        case "ondemand" | "performance":
<<<<<<< HEAD
            cmd = f"ssh {KEYFILE} root@{freqs['host']} cpupower -c all frequency-set -g {freqs['gov']} --related --min {freqs['min']}MHz --max {freqs['max']}MHz"

        case "powersave":
            cmd = f"ssh {KEYFILE} root@{freqs['host']} cpupower -c all frequency-set -g {freqs['gov']} --related --min {freqs['min']}MHz --max {freqs['min']}MHz"
=======
            cmd = f"ssh {KEYFILE} {USER}@{freqs['host']} cpupower -c all frequency-set -g {freqs['gov']} --related --min {freqs['min']}MHz --max {freqs['max']}MHz"

        case "powersave":
            cmd = f"ssh {KEYFILE} {USER}@{freqs['host']} cpupower -c all frequency-set -g {freqs['gov']} --related --min {freqs['min']}MHz --max {freqs['min']}MHz"
>>>>>>> cfa0ea7958a516dc7b07be0b8a7abe2e93eb57a9

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
    parser.add_argument('nodes', type=str, help='host(s), nodeset syntax')

    return parser.parse_args()


def set_freqs(host, gouverneur):
    """
<<<<<<< HEAD
        set min/max frequencies according to CPU family
        return a dict{'min': int, 'max': int, 'gov': powersave|ondemand|performance}
=======
        set min/max frequencies according to NodeSet/CPU family
        return a dict{'host': host, 'min': int, 'max': int, 'gov': powersave|ondemand|performance}
>>>>>>> cfa0ea7958a516dc7b07be0b8a7abe2e93eb57a9
        or return False
    """
    frequencies = {}
    match host:
        #
        # cluster X5
        #
        case hosts if hosts in NodeSet('x5570comp[1-2]'):
            # Intel X5570
            frequencies['host'] = host
            frequencies['min'] = "1600"
            frequencies['max'] = "2930"
            frequencies['gov'] = gouverneur
<<<<<<< HEAD

=======
>>>>>>> cfa0ea7958a516dc7b07be0b8a7abe2e93eb57a9
        #
        # visu et specials
        #
        case host if host in NodeSet('lensr650'):
            # Intel Gold 6444Y
            frequencies['host'] = host
            frequencies['min'] = "800"
            frequencies['max'] = "3601"
            frequencies['gov'] = gouverneur

        case host if host in NodeSet('r740flix[1-4],r740gpu[06-09]'):
            # Intel Silver 4215R
            frequencies['host'] = host
            frequencies['min'] = "1200"
            frequencies['max'] = "3200"
            frequencies['gov'] = gouverneur
            print(f"cannot do on {host}")
            return False

        case host if host in NodeSet('r740cssi,r740visu,r740cral'):
            # Intel Gold 5122
            frequencies['host'] = host
            frequencies['min'] = "1200"
            frequencies['max'] = "3600"
            frequencies['gov'] = gouverneur
            print(f"cannot do on {host}")
            return False

        case host if host in NodeSet('r640cral'):
            # Intel Gold 6148
            frequencies['host'] = host
            frequencies['min'] = "1200"
            frequencies['max'] = "2400"
            frequencies['gov'] = gouverneur
            print(f"cannot do on {host}")
            return False

        case host if host in NodeSet('cumulonimbus'):
            # Intel Platinum 8358
            frequencies['host'] = host
            frequencies['min'] = "1200"
            frequencies['max'] = "2600"
            frequencies['gov'] = gouverneur
            print(f"cannot do on {host}")
            return False
<<<<<<< HEAD

=======
>>>>>>> cfa0ea7958a516dc7b07be0b8a7abe2e93eb57a9
        #
        # cluster E5
        #
        case host if host in NodeSet('c8220node[1-48,57-202],c6320node[201-212]'):
            # Intel E5-2670, Intel E5-2697Av4
            frequencies['host'] = host
            frequencies['min'] = "1200"
            frequencies['max'] = "2601"
            frequencies['gov'] = gouverneur

        case host if host in NodeSet('c8220node[49-56]'):
            # Intel E5-2650v2
            frequencies['host'] = host
            frequencies['min'] = "1200"
            frequencies['max'] = "2600"
            frequencies['gov'] = gouverneur

        case host if host in NodeSet('e5-2667v4comp[1-2],c6320node[1-24,101-124]'):
            # Intel E5-2667v4
            frequencies['host'] = host
            frequencies['min'] = "1200"
            frequencies['max'] = "3200"
            frequencies['gov'] = gouverneur
<<<<<<< HEAD

=======
>>>>>>> cfa0ea7958a516dc7b07be0b8a7abe2e93eb57a9
        #
        # cluster E5-GPU
        #
        case host if host in NodeSet('r730gpu[01-24]'):
            # Intel E5-2637v3
            frequencies['host'] = host
            frequencies['min'] = "1200"
            frequencies['max'] = "3500"
            frequencies['gov'] = gouverneur
        #
        # cluster Lake
        #
        case host if host in NodeSet('m6142comp[1-2],c6420node[001-060,171-174]'):
            # Intel Gold 6142 2.60GHz
            frequencies['host'] = host
            frequencies['min'] = "1000"
            frequencies['max'] = "2600"
            frequencies['gov'] = gouverneur

        case host if host in NodeSet('cl6226comp[1-2],r740bigmem201,c6420node[061-168]'):
            # Intel 6226R CPU @ 2.90GHz
            frequencies['host'] = host
            frequencies['min'] = "1000"
            frequencies['max'] = "2900"
            frequencies['gov'] = gouverneur

        case host if host in NodeSet('cl5218comp[1-2],c6420node[201-204],xlr178node[001-106,109-110,119-122]'):
            # Intel Gold 5118 2.30GHz & Gold 5218 CPU @ 2.30GHz
            frequencies['host'] = host
            frequencies['min'] = "1000"
            frequencies['max'] = "2300"
            frequencies['gov'] = gouverneur

        case host if host in NodeSet('cl6242comp[1-2]'):
            # Gold 6242 CPU @ 2.80GHz
            frequencies['host'] = host
            frequencies['min'] = "1200"
            frequencies['max'] = "2800"
            frequencies['gov'] = gouverneur

        case host if host in NodeSet('xlr170node[001-010,013-036,037-060,061-072]'):
            # Gold 6242 CPU @ 2.80GHz
            # flix ! change governor
            frequencies['host'] = host
            frequencies['min'] = "1200"
            frequencies['max'] = "2800"
            frequencies['gov'] = "performance"
            return False
        #
        # cluster Epyc
        #
        case host if host in NodeSet('c6525node[001-014]'):
            # AMD EPYC 7702
            frequencies['host'] = host
            frequencies['min'] = "1500"
            frequencies['max'] = "2000"
            frequencies['gov'] = gouverneur
        #
        # cluster Cascade
        #
        case host if host in NodeSet('s92node[61-78,163-196]'):
            # Intel Platinum 9242
            # flix ! change governor
            frequencies['host'] = host
            frequencies['min'] = "1000"
            frequencies['max'] = "2300"
            frequencies['gov'] = "performance"
            return False

        case host if host in NodeSet('s92node[01-60,79-90,103-150]'):
            # Intel Platinum 9242
            frequencies['host'] = host
            frequencies['min'] = "1000"
            frequencies['max'] = "2300"
            frequencies['gov'] = gouverneur

        # None of the above
        case _:
            print(f"Host not found in Host/CPU tree: {host}")
            return False

    return frequencies


if __name__ == '__main__':
    """ """
    args = get_args()
    # debug
    if args.debug:
        debug = True
        print(args)

    fanout = args.fanout
    timeout = args.timeout

    if args.keyfile:
        KEYFILE = '-o "IdentitiesOnly=yes" -i /home/ltaulell/.ssh/cpupower-ecdsa'

    nodes = NodeSet(args.nodes)
    if debug:
        print(f"{nodes}")

    for node in nodes:
        gov = args.governor[0]
        if debug:
            print(f"{gov}")
        result = set_freqs(node, gov)
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
