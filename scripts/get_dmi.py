#!/usr/bin/env python3


# Authors: J.Barilone
# Copyright J.Barilone 2023
# Proofreader: L.Taulelle
# SPDX-License-Identifier: MIT

"""
POC: use subprocess, ClusterShell  py-dmidecode
This program can be used to retrieve information from dmidecode
on remote servers.

usage: PROGRAM [-n] [-c] [-C] [-d][-f] [-h][-H] [-m]][-M] [-n][-p] [-r] {-s}
"""

import argparse
import subprocess
from pprint import pprint

from dmidecode import DMIParse
from ClusterShell.NodeSet import NodeSet


def get_args():
    """
        Flag options available
    """
    parser = argparse.ArgumentParser(description='Ask a host for DMI data')
    parser.add_argument('-c', '--cpu_num', action='store_true', help="Affiche nombre de CPUs")
    parser.add_argument('-C', '--total_enabled_cores', action='store_true', help="Affiche nombre de coeur")
    parser.add_argument('-d', '--debug', action='store_true', help='Active le debug')
    parser.add_argument('-f', '--firmware', action='store_true', help="Affiche firmware")
    parser.add_argument('-H', '--host', action='store_true', help='hostname')
    parser.add_argument('-m', '--manufacturer', action='store_true', help="Affiche manufacturer")
    parser.add_argument('-M', '--model', action='store_true', help="Affiche model")
    parser.add_argument('-n', nargs=1, type=str, required=True, help="select nodeset")
    parser.add_argument('-p', '--cpu_type', action='store_true', help="Affiche type de CPU")
    parser.add_argument('-r', '--total_ram', action='store_true', help="Affiche RAM")
    parser.add_argument('-s', '--serial_number', action='store_true', help="serial number")
    return parser.parse_args()


def get_data(host, debug=False):
    """ use subprocess for remote connection """
    CMD = f"ssh root@{host} dmidecode"
    toto = subprocess.run(CMD, capture_output=True, shell=True, check=True, text=True)
    if debug:
        pprint(toto)
    return toto.stdout


if __name__ == '__main__':
    """ """
    args = get_args()
    if args.debug:
        debug = True
        print(args)
    else:
        debug = False
    if args.n:
        if debug:
            print(args.n)
        nodeset = NodeSet(args.n[0])
    if debug:
        print(nodeset)

    for node in nodeset:
        raw = get_data(node, debug=debug)
        if debug:
            pprint(raw)
        dmi = DMIParse(raw)
        if debug:
            pprint(dmi.data)
        if args.cpu_num:
            print(f"Number of Socket(s): {dmi.cpu_num()}")
        if args.total_enabled_cores:
            print(f"Number of Core(s) Enabled: {dmi.total_enabled_cores()}")
        if args.firmware:
            # print(f"Version Firmware: {dmi.firmware()}")
            # Return BIOS value
            for v in dmi.data.values():
                if 'BIOS Revision' in v.keys():
                    toto = v['BIOS Revision']
                    print(f"Version Firmware: {toto}")
        # Print Info
        if args.manufacturer:
            print(f"Manufacturer: {dmi.manufacturer()}")
        if args.model:
            print(f"Model: {dmi.model()}")
        if args.cpu_type:
            print(f"Processor: {dmi.cpu_type()}")
        if args.total_ram:
            print(f"Total RAM (GB): {dmi.total_ram()}")
        if args.serial_number:
            print(f"Serial Number: {dmi.serial_number()}")
