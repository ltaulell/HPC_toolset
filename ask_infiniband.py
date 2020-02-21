#!/usr/bin/env python3
# coding: utf-8

# $Id: ask_infiniband.py 2819 2020-02-21 15:01:19Z ltaulell $
# SPDX-License-Identifier: CECILL-B

"""
    Ask nodes for fw rev and PSID
    make a nice table
    if filename, save in as csv
    else save in default filename as csv

    hostname,fw_ver,board_id
    ibv_devinfo | grep fw_ver
    ibv_devinfo | grep board_id
"""

import argparse
import csv
import sys

import execo
from ClusterShell.NodeSet import NodeSet


entetes = ['hostname', 'fw_ver', 'board_id', 'serial_number']  # french for headers
outlist = []


def main():
    """ for each node, execo.Ssh for info
        fill a list of list (outlist)
        write that outlist to csv
    """
    args = get_options()
    # debug
    if args.d:
        debug = True
        print(args)
    else:
        debug = False

    outlist.append(entetes)
    nodes = NodeSet(args.nodes)

    for node in nodes:
        print(node)
        cmd_fw = 'ibv_devinfo | grep fw_ver'
        res_fw = ask_node(cmd_fw, node, debug)
        cmd_id = 'ibv_devinfo | grep board_id'
        res_id = ask_node(cmd_id, node, debug)
        cmd_sn = 'lspci -vvv | grep -e "\[SN\] Serial number"'
        res_sn = ask_node(cmd_sn, node, debug)
        outlist.append([node, res_fw, res_id, res_sn])

    if debug:
        print(outlist)

    fichier_out = args.f[0]
    write_csv_file(outlist, fichier_out)


def write_csv_file(data, outfile):
    """ write a csv file, with headers
        data must be a list of list
    """
    try:
        with open(outfile, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

    except IOError:
        execo.log.logger.error("Unable to open file: " + csvfile.name)
        sys.exit(1)


def get_options():
    """ get CLI arguments """
    parser = argparse.ArgumentParser(description='ask host(s) for infiniband informations, output a csv file')
    parser.add_argument('-d', action='store_true', help='toggle debug ON (default: no)')
    parser.add_argument('-f', nargs=1, type=str, help='file to write (default: compilation.csv)', default='compilation.csv')
    parser.add_argument('nodes', type=str, help='host(s), nodeset syntax')

    args = parser.parse_args()

    return args


def ask_node(cmd, host, debug=False):
    """ using execo, connect to host and execute cmd
        cmd be like:
            ibv_devinfo | grep fw_ver   => '\tfw_ver:\t\t\t\t2.11.310\r\n'
            ibv_devinfo | grep board_id => '\tboard_id:\t\t\tHP_0280210019\r\n'
        return the last element of stdout, as a str
    """
    process = execo.SshProcess(cmd, host, {'user': 'root'}).run()
    if process.stdout == "":
        return "No connection"
    else:
        return str(process.stdout.split()[-1])


if __name__ == '__main__':
    """ GOTO main """
    main()
