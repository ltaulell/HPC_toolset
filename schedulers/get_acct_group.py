#!/usr/bin/env python3
# coding: utf-8

# PSMN: $Id: get_acct_group.py 4169 2023-10-02 13:16:16Z ltaulell $
# SPDX-License-Identifier: CECILL-B OR BSD-2-Clause

"""
Sur la base de get_acct_group.sh, remplace get_acct_group.sh
slurmdbd n'arrive pas à fournir les jobs sur l'année, il faut traiter mois par mois

for i in $(sacctmgr -nP list account format=account | xargs);
do sreport -n job sizes printjobcount Start=2022-01-01 End=2023-01-01 Accounts="${i}" | \
awk -F" " '{ SUM +=$3+$4+$5+$6+$7} END {print $2" "SUM}' ;
done

output CSV annuel
group,jobs,hours

"""

import argparse
import datetime
import calendar
import csv
import subprocess
import pprint

ENTETES = ['group', 'jobs', 'hours']
MASTER_D = {'': {'group': '', 'jobs': 0, 'hours': 0}}
EXCLUDES = ['bioensl', 'chimieucbl', 'ecl', 'ensl', 'entreprises', 'root', 'ucbl']


def get_options():
    """ get CLI arguments """
    parser = argparse.ArgumentParser(description='compile slurm stats, by date, by group, output a csv file')
    parser.add_argument('-d', action='store_true', help='toggle debug ON (default: no)')
    parser.add_argument('-f', nargs=1, type=str, help='file to write (default: accounting.csv)', default='accounting.csv')
    parser.add_argument('-y', nargs=1, type=int, help='year of stats (in YYYY form)')
    parser.add_argument('-g', nargs=1, type=str, help='group (default: all)', default='all')

    args = parser.parse_args()

    return args


def get_accounts(debug=False):
    """ get full list of slurm accounts """
    """ ACCOUNTS = $(sacctmgr -nP list account format=account | xargs) """

    CMD = "sacctmgr -nP list account format=account | xargs"
    acc_out = subprocess.check_output(CMD, shell=True, text=True)
    acc_out = str(acc_out)
    acc_clean = str(acc_out.strip("b'").strip('\\n')).split()

    # nettoyer la liste d'accounts
    for elt in EXCLUDES:
        acc_clean.remove(elt)

    if debug:
        pprint.pprint(acc_clean)

    return acc_clean


def create_dict(accounts, debug=False):
    """ create dict from accounts list """
    """ dict={'$group': {'jobs' = $jobs, 'hours' = $hours}} """

    res_dct = {str(accounts[i]): {'group': str(accounts[i]), 'jobs': 0, 'hours': 0} for i in range(0, len(accounts), 1)}

    if debug:
        pprint.pprint(res_dct)

    return res_dct


def get_hours(MASTER_D, YEAR, debug=False):
    """ get accounted hours for group(s) in MASTER_D """
    """
    nb hours par account:
    res = sreport -n cluster AccountUtilizationByUser format=Used -t Hours start=2022-01-01T00:00 end=2022-12-31T23:59 accounts=lmfa
    garder seulement res[0]
    """

    for key in MASTER_D.keys():
        debut = datetime.date(YEAR, 1, 1)
        fin = datetime.date(YEAR, 12, 31)
        CMD = f"sreport -n cluster AccountUtilizationByUser format=Used -t Hours start={debut} end={fin} accounts={key}"
        if debug:
            print(CMD)
        h_out = subprocess.check_output(CMD, shell=True, text=True)
        if h_out:
            h_out = str(h_out).split()
            if debug:
                print(h_out)
        else:
            h_out = [0]

        h_clean = int(h_out[0])

        if debug:
            print(f"{h_out}, {h_clean}")

        MASTER_D[key]['hours'] = h_clean


def get_jobs_sum(MASTER_D, YEAR, debug=False):
    """ get and compute accounted number of jobs """
    """ loop de janvier à décembre autour de start=$year-$month-01 end=$year-$month+1-01
    hint: start sous-entend T00:00:00, end-> T23:59:00

    for i in $(sacctmgr -nP list account format=account | xargs); do 
    sreport -n job sizes printjobcount Start=2022-01-01 End=2023-01-01 Accounts="${i}" | \
    awk -F" " '{ SUM +=$3+$4+$5+$6+$7} END {print $2" "SUM}' ;
    done
    """

    for key in MASTER_D.keys():
        j_key = 0
        for mois in range(1, 13):  # range est non-inclusif, remember?
            debut = datetime.date(YEAR, mois, 1)
            # calendar.monthrange(YEAR, mois)[1] -> dernier jour du mois en cours
            fin = datetime.date(YEAR, mois, calendar.monthrange(YEAR, mois)[1])

            CMD = f"sreport -n job sizes printjobcount start={debut} end={fin} accounts={key}"
            if debug:
                print(CMD)
            j_out = subprocess.check_output(CMD, shell=True, text=True)
            if j_out:
                j_out = str(j_out).split()
                if debug:
                    print(j_out)
            else:
                j_out = [0]

            # j'ai besoin de $2 à $6 inclus, en tant qu'entiers
            j_clean = sum([int(elt) for elt in j_out[2:7]])

            if debug:
                print(j_clean)

            j_key += j_clean

        MASTER_D[key]['jobs'] = j_key


def write_csv_file(outfile):
    """ write a csv file, with headers """

    for k in MASTER_D.keys():
        print(MASTER_D[k].values())
        print(dict(MASTER_D[k].items()))

    try:
        with open(outfile, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=ENTETES)
            writer.writeheader()
            for k in MASTER_D.keys():
                writer.writerow(dict(MASTER_D[k].items()))

    except IOError:
        print(f"Unable to open file: {csvfile.name}")
        exit(1)


if __name__ == '__main__':
    """ """
    args = get_options()
    if args.d:
        debug = True
        print(args)
    else:
        debug = False

    if args.y:
        YEAR = int(args.y[0])

    if 'all' in args.g:
        accounts = get_accounts(debug)
    else:
        accounts = args.g

    MASTER_D = create_dict(accounts, debug)

    get_hours(MASTER_D, YEAR, debug)

    get_jobs_sum(MASTER_D, YEAR, debug)

    if debug:
        pprint.pprint(MASTER_D)

    write_csv_file(args.f)
