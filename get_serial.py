#!/usr/bin/env python3
# coding: utf-8

# PSMN: $Id: get_serial.py 2997 2020-09-23 13:14:12Z ltaulell $
# SPDX-License-Identifier: CECILL-B OR BSD-2-Clause

""" POC: use execo to get chassis serial number from host(s)

quick & dirty

return a list of comma separated serial numbers
"""

import argparse
import execo

from ClusterShell.NodeSet import NodeSet


def get_args():
    """
        read parser and return args (as args namespace)
    """
    parser = argparse.ArgumentParser(description='Ask an host for Serial Number')
    parser.add_argument('-d', '--debug', action='store_true', help='Active le debug')
    parser.add_argument('-H', '--host', nargs=1, type=str, help='hostname(s), NodeSet syntax')

    return parser.parse_args()


def get_data(host, debug=False):
    """ use execo as a better subprocess substitute """

    cmd = "cat /sys/class/dmi/id/product_serial"

    process = execo.SshProcess(cmd, host, {'user': 'root'}, shell=False).run()

    if debug:
        print(process.stderr)

    return process.stdout


if __name__ == '__main__':
    """ """
    args = get_args()

    if args.debug:
        debug = True
        print(args)
    else:
        debug = False

    nodes = NodeSet(args.host[0])

    liste = []
    for node in nodes:
        raw = get_data(node, debug).split('\r')
        liste.append(raw[0])
    print(','.join(liste))
