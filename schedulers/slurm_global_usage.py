#!/usr/bin/env python3
# coding: utf-8
#
# $Id: slurm_global_usage.py 4265 2023-12-13 13:30:47Z ltaulell $
# SPDX-License-Identifier: BSD-2-Clause
#

""" agregate percent usage of slurm partitions, like munin plugin """

import subprocess
import datetime
import csv
import os
# from pprint import pprint

part_dict = {}

partition_cmd = 'sinfo -h -o "%R"'
partition_run = subprocess.run(partition_cmd, capture_output=True, shell=True, check=True, text=True)
partitions = list(partition_run.stdout.split())


for partition in partitions:
    part_dict[partition] = {}

    # running
    run_cmd0 = f"sinfo -h -p {partition} -e -o '%C'"
    run_cmd = ' '.join([run_cmd0, "| awk -F'/' 'BEGIN {somme=0} {somme+=($1)} END {print somme}'"])
    run_run = subprocess.run(run_cmd, capture_output=True, shell=True, check=True, text=True)
    part_dict[partition]['run'] = run_run.stdout.strip()
    # total core
    total_cmd0 = f"sinfo -h -p {partition} -e -o '%C'"
    total_cmd = ' '.join([total_cmd0, "| awk -F'/' 'BEGIN {somme=0} {somme+=($4)} END {print somme}'"])
    total_run = subprocess.run(total_cmd, capture_output=True, shell=True, check=True, text=True)
    part_dict[partition]['total'] = total_run.stdout.strip()
    # unavailable
    unavail_cmd0 = f"sinfo -h -p {partition} -e -o '%C'"
    unavail_cmd = ' '.join([unavail_cmd0, "| awk -F'/' 'BEGIN {somme=0} {somme+=($3)} END {print somme}'"])
    unavail_run = subprocess.run(unavail_cmd, capture_output=True, shell=True, check=True, text=True)
    part_dict[partition]['unavailable'] = unavail_run.stdout.strip()

part_dict['global'] = {}
global_run_cmd = "sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($1)} END {print somme}'"
global_run_run = subprocess.run(global_run_cmd, capture_output=True, shell=True, check=True, text=True)
part_dict['global']['run'] = global_run_run.stdout.strip()

global_total_cmd = "sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($4)} END {print somme}'"
global_total_run = subprocess.run(global_total_cmd, capture_output=True, shell=True, check=True, text=True)
part_dict['global']['total'] = global_total_run.stdout.strip()

global_unavail_cmd = "sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($3)} END {print somme}'"
global_unavail_run = subprocess.run(global_unavail_cmd, capture_output=True, shell=True, check=True, text=True)
part_dict['global']['unavailable'] = global_unavail_run.stdout.strip()

for partition in part_dict.keys():
    part_dict[partition]['percent'] = (int(part_dict[partition]['run']) * 100) / (int(part_dict[partition]['total']) - int(part_dict[partition]['unavailable']))

date = str(datetime.datetime.now().timestamp())

# print(date)
# pprint(part_dict)
# pprint(part_dict.keys())

entetes = ['date']
result = {'date': date}
for key in part_dict.keys():
    entetes.append(key)
    for k, v in part_dict[key].items():
        if k == 'percent':
            result[key] = f"{v:.2f}"

# print(entetes)
# print(result)

fichier = 'percent_usage.csv'
if not os.path.exists(fichier):
    nohead = True
else:
    nohead = False

try:
    with open(fichier, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=entetes)

        if nohead:
            writer.writeheader()

        writer.writerow(result)

except IOError as e:
    print(e)
