#!/usr/bin/env python3
# coding: utf-8
#
# $Id: map_GUID.py 3038 2020-11-16 09:16:19Z ltaulell $
# SPDX-License-Identifier: BSD-2-Clause
#

"""
create a "GUID hostname" map for DOT visualisation
"""

import argparse
import sys

import execo
from ClusterShell.NodeSet import NodeSet

CMD = 'ibstat | grep -e "Node GUID" | awk -F"0x" \'{print $2}\''

def get_args():
    """ get arguments from CLI """
    parser = argparse.ArgumentParser(description='Create IB Map >> file')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='toggle debug on')
    parser.add_argument('host', type=str, help='host(s), nodeset syntax')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    if args.debug:
        execo.log.logger.setLevel('DEBUG')
    else:
        execo.log.logger.setLevel('ERROR')

    nodes = NodeSet(args.host)

    for node in nodes:
        try:
            process = execo.SshProcess(CMD, node, {'user': 'root', 'nolog_error': True, 'ignore_error': True}, shell=True).run()
        except execo.exception.ProcessesFailed:
            execo.log.logger.exception('Process error')
            sys.exit(1)
        if process.stdout == '':
            print('# No connection {}'.format(node))
        else:
            # only need short GUID, might be redundant with awk
            print('H-{} {}'.format(process.stdout.split('0x')[-1].strip(), node))

