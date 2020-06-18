#!/usr/bin/env python3
# coding: utf-8

# PSMN: $Id: test_ipmitool.py 2933 2020-06-18 13:37:27Z ltaulell $
# SPDX-License-Identifier: CECILL-B OR BSD-2-Clause

""" use ipmitool to get data from BMC interface 

this is a POC, output to a CSV file, for some metrology

"""

# import sys
import argparse
import execo
import csv
import time
import os
from pprint import pprint


def get_data(host, user, password, debug=False):
    host = host + '-mngt'
    user = user
    password = password

    cmd = "ipmitool -e \& -I lanplus -U {} -P {} -H {} sensor".format(user, password, host)
    process = execo.Process(cmd, shell=False)
    process.run()
    # split process.stdout line by line
    if debug:
        pprint(process.stderr)
    return process.stdout.split('\n')


def get_args():
    """
        read parser and return args (as args namespace)
    """
    parser = argparse.ArgumentParser(description='Ask an host for IPMI data (lanplus active by default)')
    parser.add_argument('-d', '--debug', action='store_true', help='Active le debug')
    parser.add_argument('-H', '--host', nargs=1, type=str, help='hostname')
    parser.add_argument('-U', '--user', nargs=1, type=str, help='IPMI user')
    parser.add_argument('-P', '--password', nargs=1, type=str, help='IMPI password')

    return parser.parse_args()


if __name__ == '__main__':
    """ """
    args = get_args()
    if args.debug:
        debug = True
        print(args)
    else:
        debug = False

    result = []
    sensors = get_data(args.host[0], args.user[0], args.password[0], debug=debug)
    for ligne in sensors:
        if ligne.split('|')[0] == 'Temp             ':
            result.append(ligne.split('|')[1].strip())
        if ligne.split('|')[0] == 'Pwr Consumption  ':
            result.append(ligne.split('|')[1].strip())
    if debug:
        pprint(result)

    fichier = args.host[0] + '-metrologie.csv'
    if os.path.exists(fichier):
        noheader = False
    else:
        noheader = True

    with open(fichier, 'a', newline='') as csvfile:
        entetes = ['date', 'CPU1', 'CPU2', 'Pwr']
        writer = csv.DictWriter(csvfile, fieldnames=entetes)
        if noheader:
            if debug:
                print(noheader)
            writer.writeheader()

        date = time.time()
        writer.writerow({'date': date,
                         'CPU1': result[0],
                         'CPU2': result[1],
                         'Pwr': result[2],
                         })
