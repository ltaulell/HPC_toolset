#!/usr/bin/env python3
# coding: utf-8

# PSMN: $Id: get_ipmitool.py 2940 2020-06-23 11:36:55Z ltaulell $
# SPDX-License-Identifier: CECILL-B OR BSD-2-Clause

""" POC: use ipmitool to get data from BMC interface

Lot of hardcoded things
"""

import argparse
import execo
import csv
import time
import os
from pprint import pprint


def get_data(host, user, password, debug=False):
    """ use execo as a better subprocess substitute """
    host = host + '-mngt'
    user = user
    password = password

    cmd = "ipmitool -I lanplus -U {} -P {} -H {} sensor".format(user, password, host)
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
        # we care about first column's value
        clef = ligne.split('|')[0].strip()
        valeur = ligne.split('|')[1].strip()

        # adapt matching to what you want
        # if clef == 'Memory':  # test for 'na'
        if clef == 'Temp':  # original one
            # beware of 'na' values
            if valeur == 'na':
                result.append(0)
            else:
                result.append(valeur)

        if clef == 'Pwr Consumption':
            if valeur == 'na':
                result.append(0)
            else:
                result.append(valeur)

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
