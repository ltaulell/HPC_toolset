#!/usr/bin/env python3

# Authors: J.Barilone
# Copyright J.Barilone 2023
# Proofreader: L.Taulelle
# SPDX-License-Identifier: MIT

"""

used with nodeset and execo modules

This program will retrieve firmware data from multiple remote hosts
and print to csv file.

usage: PROG [-n] [-o] [-h] [-d]
"""

import execo
from ClusterShell.NodeSet import NodeSet

import csv
from datetime import datetime
import os
import argparse
import pprint

# get date and format as string
date = datetime.now().strftime("%Y-%m")


# NODES = {'': {'idrac': '', 'BIOS': ''},}
NODES = {}
# TOTO = []


def get_flags():
    """ Available flags """
    parser = argparse.ArgumentParser()
    # -n arg is required
    parser.add_argument('-n', nargs=1, type=str, required=True, help="select nodeset")
    parser.add_argument('-o', type=str, nargs=1, required=False, help="choose filename (default=YYYY-mm_node_firmware.csv)", default=[f"{date}_node_firmware.csv"])
    parser.add_argument('-d', action='store_true', help="toggle debug")
    args = parser.parse_args()
    return args


def ask_node(cmd, host, shell=False):
    """ Use of execo to connect to remote host """
    if not cmd:
        cmd = "hostname"
    process = execo.SshProcess(cmd, host, {'user': 'root'}, shell=shell).run()
    # split process.stdout line by line
    # pprint.pprint(process.stdout)
    return str(process.stdout)


if __name__ == '__main__':
    """ """
    args = get_flags()

    if args.d:
        debug = True
        print(args)
    else:
        debug = False
    if args.n:
        nodeset = NodeSet(args.n[0])
    if debug:
        print(nodeset)

    # Create for loop to run commands on each node
    for node in nodeset:
        TOTO = []
        cmd = "hostname"
        result = ask_node(cmd, node)
        result = result.strip('\r\n')
        if debug:
            print(result)
        TOTO.append(node)
        # cmd for BIOS information
        cmd = 'dmidecode | grep -e "Version: " | head -n 1'
        result = ask_node(cmd, node, shell=True)
        result = result.strip('\t').strip('\r\n')
        result = result.split(':')[1].strip()
        if debug:
            print(result)
        TOTO.append(result)
        # cmd for iDRAC version
        cmd = 'ipmitool mc info | grep -e "Firmware Revision"'
        result = ask_node(cmd, node, shell=True)
        result = result.split(':')[1].strip()
        if debug:
            print(result)
        TOTO.append(result)
        if debug:
            pprint.pprint(TOTO)
            print(args.o[0])
        if os.path.exists(args.o[0]):
            noheader = False
        else:
            noheader = True

        # write csv with headers
        with open(args.o[0], 'a', newline='') as csvfile:
            header = ['Name', 'BIOS', 'iDRAC']
            writer = csv.DictWriter(csvfile, fieldnames=header)
            if noheader:
                writer.writeheader()

            # fill dictionary with elements from list
            writer.writerow({'Name': TOTO[0],
                             'BIOS': TOTO[1],
                             'iDRAC': TOTO[2]})
