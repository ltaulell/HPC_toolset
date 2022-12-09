#!/usr/bin/env python3
# coding: utf-8

# $Id: top_ten.py 3876 2022-12-09 13:54:13Z ltaulell $
# SPDX-License-Identifier: CECILL-B

"""
    display a slurm top ten user by:
    * user, jobs, cpus pending
    * user, jobs, cpus running

    squeue --noheader --states=PENDING|RUNNING --format="%.8u %.4C"

"""

import argparse
import subprocess

from pprint import pprint

users = {}


def get_options():
    """ get CLI arguments """
    parser = argparse.ArgumentParser(description='Display slurm Top Ten users')
    parser.add_argument('-d', action='store_true', help='toggle debug ON (default: no)')
    group1 = parser.add_mutually_exclusive_group(required=False)
    group1.add_argument('-j', action='store_true', help='sort by jobs count')
    group1.add_argument('-c', action='store_true', help='sort by cpus count (default)')
    group2 = parser.add_mutually_exclusive_group(required=True)
    group2.add_argument('-p', action='store_true', help='pending jobs')
    group2.add_argument('-r', action='store_true', help='running jobs', required=False)

    return parser.parse_args()


args = get_options()

if args.d:
    print(f'{args}')

if args.p:
    CMD = "squeue --noheader --states=PENDING --format=\"%.8u %.4C\" "

if args.r:
    CMD = "squeue --noheader --states=RUNNING --format=\"%.8u %.4C\" "

get_list = subprocess.run(CMD, capture_output=True, shell=True, check=True, text=True)

if args.d:
    print(f'{get_list}')

for line in get_list.stdout.strip().split('\n'):
    line = line.strip().split(' ')

    if args.d:
        print(f'{line}')

    # cleanup None values
    liste = list(filter(None, line))

    if args.d:
        print(f'{liste}')
        for i, v in enumerate(liste):
            print(i, v)

    user = liste[0]

    if args.d:
        print(f'user: {user}')

    if user not in users.keys():
        users[user] = {'jobs': 0, 'cpus': 0, }
        users[user]['jobs'] += 1
        users[user]['cpus'] += int(liste[1])

        if args.d:
            print(f'tab: {users}')

    else:
        users[user]['jobs'] += 1
        users[user]['cpus'] += int(liste[1])

if args.d:
    pprint(users)

# using sorted(), sort nested dictionary by key
if args.j:
    res = sorted(users.items(), key=lambda x: x[1]['jobs'], reverse=True)[:10]
else:
    res = sorted(users.items(), key=lambda x: x[1]['cpus'], reverse=True)[:10]

if args.d:
    pprint(res)

print(' user, cpus, jobs')
for elt in res:
    print(f" {elt[0]}, {elt[1]['cpus']}, {elt[1]['jobs']}")
