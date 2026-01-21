#!/usr/bin/env python3
# coding: utf-8

# PSMN: $Id: get_detail_acct_user.py 4800 2025-03-12 14:35:25Z ltaulell $
# SPDX-License-Identifier: CECILL-B OR BSD-2-Clause

"""
retrouve le détail de l'accounting d'un utilisateur, par année
- user association
sacctmgr -nP show user withassoc format=account,user,defaultaccount where user=$USER
sacctmgr -nP show user withassoc format=defaultaccount where user=$USER
- id de jobs (quarts de mois, comme get_acct_group.py)
sacct --starttime=2023-01-01-00:00:00 --endtime=2023-01-31-23:59:59 --accounts=$ACCOUNT --format=Account,User,JobID
- sur quel(s) node(s)
sacct -n -j $JOB_ID.batch --format=NodeList%-30s
- total hours (fool me! only on $JOB_ID.batch) else error, accounting = 0
if TotalCPU <= NCPUS x ElapsedRaw then OK
sacct -j $JOB_ID.batch --format=TotalCPU,NCPUS,ElapsedRaw

sacct debug output : -lp | column -s '|' -t | most

output to csv "lab_user_year.csv"
"""


import argparse
import subprocess
import datetime
import calendar
import csv
import yaml
import sys

from ClusterShell.NodeSet import NodeSet
from pprint import pprint


debug = False
verbose = False
JOBS_DICT = {}
ACCT = {}
BAD_JOBS = []
ENTETESV = ['nodeset', 'jobs', 'jobs_id', 'hours']
ENTETES = ['nodeset', 'jobs', 'hours']
REFERENTIEL = "clusters.yml"
NODESREF = {}


def get_options():
    """ get CLI arguments """
    parser = argparse.ArgumentParser(description='compile slurm stats, by year, by user')
    parser.add_argument('-d', '--debug', action='store_true', help='toggle debug ON (default: no)')
    parser.add_argument('-v', '--verbose', action='store_true', help='toggle verbose ON (default: no)')
    # parser.add_argument('-o', '--outfile', nargs=1, type=str, help='file to write (default: accounting.csv)', default=['accounting.csv'])
    parser.add_argument('-r', '--referentiel', type=str, help='referential file', default=['clusters.yml'])
    parser.add_argument('-y', '--year', nargs=1, type=int, help='year of stats (in YYYY form)')
    parser.add_argument('-u', '--user', nargs=1, type=str, help='user (no default)')

    args = parser.parse_args()

    return args


def execute(cmd, debug=False):
    """
        use subprocess to execute cmd
        return unmodified output
    """

    try:
        result_out = subprocess.check_output(cmd, shell=True, text=True)
    except subprocess.CalledProcessError:
        result_out = None
        pass

    return result_out


def load_yaml_file(yamlfile):
    """
    load data from a yaml file, using safe_load, return a dict{}.

    yamlfile is mandatory. Throw yaml errors, if any.

    import sys
    import yaml

    """
    try:
        with open(yamlfile, 'r') as fichier:
            contenu = yaml.safe_load(fichier)
            return contenu
    except IOError:
        print("Unable to open file: {}".format(fichier.name))
        sys.exit(1)
    except yaml.YAMLError as erreur:
        if hasattr(erreur, 'problem_mark'):
            mark = erreur.problem_mark
            # print("YAML error position: (%s:%s) in" % (mark.line + 1, mark.column + 1), fichier.name)
            print('YAML error position: ({}:{}) in {}'.format(mark.line + 1, mark.column + 1, fichier.name))
        sys.exit(1)


def get_accounts(USER, debug=False):
    """
        find account(s) for user
        return a list
    """
    cmd = f"sacctmgr -nP show user withassoc format=account where user={USER}"
    if debug:
        print(cmd)

    acc_out = execute(cmd, debug)

    if debug:
        print(acc_out)
        print(type(acc_out))
    acc_clean = list(str(acc_out.strip('\\n')).split())
    if debug:
        print(acc_clean)
    return acc_clean


def get_jobids(account, USER, YEAR, debug=False):
    """
        get jobids from current user/account association
        ask sacct by quarters of month to avoid overload
        modify JOBS_DICT
    """
    global JOBS_DICT
    # user_short = USER[:8]  # grep won't work with 8+ long logins because of sacct output

    for mois in range(1, 13):  # range est non-inclusif, remember?
        # découper mois en 4 morceaux se recouvrant (and we do handle duplicates)
        start = (1, 7)
        middle = (7, 14)
        third = (14, 21)
        last = (21, calendar.monthrange(YEAR, mois)[1])
        for un, deux in start, middle, third, last:
            debut = datetime.date(YEAR, mois, un)
            fin = datetime.date(YEAR, mois, deux)

            cmd = ''.join(["sacct -n --starttime=", str(debut),
                           " --endtime=", str(fin),
                           " --accounts=", account,
                           " --format=User%16s,JobID | grep ", USER,
                           " | awk '{print $2}'"])
            if debug:
                print(cmd)

            jobs_out = execute(cmd, debug)
            # fast debug (with duplicate jobs)
            # jobs_out = """1238240\n1305200\n1305200\n1355639\n1369272\n1369272\n2461221\n4147733\n"""
            # jobs_out = """7511117\n7511144\n7514253\n7515069\n"""

            if debug:
                print(jobs_out)
            jobs_clean = list(str(jobs_out.strip('\\n')).split())

            for job in jobs_clean:
                # handle duplicates job_ids
                if job not in JOBS_DICT.keys():
                    # progress bar
                    print('.', end='')
                    JOBS_DICT[job] = {'account': (account, USER)}


def get_details_job(debug=False):
    """
        for each jobid in global JOBS_DICT
        get details: nodes, hours, verif
    """
    global JOBS_DICT, BAD_JOBS

    for job in JOBS_DICT.keys():
        # CPUTimeRAW (in seconds) or TotalCPU (day-h:m:s)
        # ElapsedRaw (in seconds) for sure
        # AllocCPUS or NCPUS (int)
        # UserCPU (day-h:m:s)
        # cmd = f"sacct -n -j {job}.batch --format=NodeList%-30s,TotalCPU%-13s,NCPUS%5s,ElapsedRaw%8s"
        cmd = f"sacct -n -j {job} --duplicates --format=NodeList%-60s,CPUTimeRAW%-13s,NCPUS%5s,ElapsedRaw%8s"
        if debug:
            print(cmd)

        details_out = execute(cmd, debug)

        if debug:
            print(details_out)

        # simply split output
        try:
            # only keep first line
            # nodes_out, TotalCPU, NCPUS, ElapsedRaw = details_out.split()
            nodes_out, CPUTimeRAW, NCPUS, ElapsedRaw = details_out.split('\n')[0].split()

            nodes_clean = str(nodes_out.strip())
            if debug:
                print(type(nodes_clean))

            JOBS_DICT[job]['nodes'] = nodes_clean

            # here stands the devil
            # split in 2, then 3, TotalCPU/UserCPU is a timedelta, NCPUS is an int, Elapsed is a timedelta
            # WARNING: TotalCPU can be 'day-h:m:s', or 'h:m:s', or 'm:seconds.milliseconds'
            # day, CPU = TotalCPU.split('-')
            # hour, min, sec = CPU.split(':')
            """ Nah, stick to CPUTimeRAW
            try:
                jour, CPUreste = TotalCPU.split('-')
                heure, minute, seconde = CPUreste.split(':')
            except ValueError:
                jour = 0
                try:
                    heure, minute, seconde = TotalCPU.split(':')
                except ValueError:
                    heure = 0
                    minute, sec_sale = TotalCPU.split(':')
                    seconde = int(float(sec_sale))

            if debug:
                print(f"day,H,m,s: {jour}, {heure}, {minute}, {seconde}")

            td_total = datetime.timedelta(days=int(jour),
                                          hours=int(heure),
                                          minutes=int(minute),
                                          seconds=int(seconde)
                                          )
            """
            td_total = datetime.timedelta(seconds=int(CPUTimeRAW))
            computed_time = (int(NCPUS) * int(ElapsedRaw))
            td_computed = datetime.timedelta(seconds=computed_time)

            if td_total <= td_computed:
                JOBS_DICT[job]['minutes'] = int(td_total.total_seconds() / 60)

        except (ValueError, AttributeError):
            """ generaly 'no nodes assigned' and 0 CPUTime """
            if debug:
                print(f"problem with {job}")
            BAD_JOBS.append(job)
            JOBS_DICT[job]['nodes'] = None
            JOBS_DICT[job]['minutes'] = 0


def get_nodes_job(nodes, debug=False):
    """
        get groupAltName for node
        return groupAltName
    """

    for node in nodes:
        for cluster in NODESREF.keys():
            for group in NODESREF[cluster].keys():
                nodeset = NodeSet(group)
                if node in nodeset:
                    # premier noeud qui match
                    if debug:
                        print(f"{nodes} in {NODESREF[cluster][group]['groupAltName']}")
                    return str(NODESREF[cluster][group]['groupAltName'])


def update_acct_dict(account, nodeset, jobid=None, minutes=0, verbose=False):
    """ update global ACCT values for account and nodeset key pair

    Args:
        account: The account tuple (string).
        nodeset: The nodeset name (string).
        jobid: Optional job ID to append (string, only if verbose is True).
        minutes: The number of minutes to add (integer).
        verbose: Whether to track job IDs (boolean).
    """
    global ACCT

    # Get the account dictionary (create if it doesn't exist)
    account_data = ACCT.setdefault(account, {})
    # Get the group dictionary within the account (create if it doesn't exist)
    group_data = account_data.setdefault(group, {'jobs': 0, 'jobs_id': [], 'minutes': 0})
    # Update jobs and minutes for the group
    group_data['jobs'] += 1
    group_data['minutes'] += minutes

    # Add job ID if verbose is True
    if verbose:
        group_data['jobs_id'].append(jobid)


def write_csv_file(YEAR, verbose=False, debug=False):
    """ write a csv file, with headers """
    global ACCT

    for labo, user in ACCT.keys():
        if verbose:
            outfile = f"{labo}_{user}_{YEAR}+verbose.csv"
        else:
            outfile = f"{labo}_{user}_{YEAR}.csv"
        if debug:
            print(outfile)

        if debug:
            for k in ACCT[account].keys():
                print(f"{k}: {list(ACCT[account][k].values())}")
                print(dict(ACCT[account][k].items()))

        try:
            with open(outfile, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"')
                if verbose:
                    writer.writerow(ENTETESV)
                else:
                    writer.writerow(ENTETES)
                for k in ACCT[account].keys():
                    nodeset = k
                    jobs = f"{ACCT[account][k]['jobs']}"
                    hours = f"{(ACCT[account][k]['minutes'] / 60):.0f}"
                    if verbose:
                        ids = f"{ACCT[account][k]['jobs_id']}"
                        writer.writerow([nodeset, jobs, ids, hours])
                    else:
                        writer.writerow([nodeset, jobs, hours])

        except IOError:
            print(f"Unable to open file: {csvfile.name}")
            sys.exit(1)


def write_bad_job(debug=False):
    """ write list of bad jobid """
    global ACCT, BAD_JOBS
    for labo, user in ACCT.keys():
        outfile = f"{labo}_{user}_badjob.lst"
        try:
            with open(outfile, 'wt') as fichier:
                fichier.write('\n'.join(BAD_JOBS))
                fichier.write('\n')
        except (IndexError, FileNotFoundError, EnvironmentError) as erreur:
            print(f"{erreur}, with {outfile}")


if __name__ == '__main__':
    """ """
    args = get_options()
    if args.debug:
        debug = True
        print(args)
    if args.verbose:
        verbose = True

    if args.referentiel:
        REFERENTIEL = args.referentiel[0]

    NODESREF = load_yaml_file(REFERENTIEL)

    if args.year:
        YEAR = int(args.year[0])

    if args.user:
        USER = str(args.user[0])

    accounts = get_accounts(USER, debug)

    for account in accounts:
        get_jobids(account, USER, YEAR, debug)  # modify JOBS_DICT

    get_details_job(debug)  # modify JOBS_DICT

    if debug:
        pprint(JOBS_DICT)

    for jobid in JOBS_DICT.keys():
        account = JOBS_DICT[jobid]['account']
        nodes = NodeSet(JOBS_DICT[jobid]['nodes'])  # on compare des NodeSet()
        group = get_nodes_job(nodes, debug)
        minutes = JOBS_DICT[jobid]['minutes']

        if debug:
            print(f'debug: {jobid}, {account}, {nodes}, {group}, {minutes}')

        update_acct_dict(account, group, jobid, minutes, verbose)

    if debug:
        pprint(ACCT)

    # write csv result file
    write_csv_file(YEAR, verbose, debug)

    # print final résumé
    for account in ACCT.keys():
        print(f"\nlabo, user: {account}")
        for group in ACCT[account].keys():
            print(f"  nodeset: {group}")
            print(f"    jobs: {ACCT[account][group]['jobs']}")
            if verbose:
                print(f"    jobs list: {ACCT[account][group]['jobs_id']}")
            print(f"    hours: {(ACCT[account][group]['minutes'] / 60):.0f}")

    if BAD_JOBS:
        if debug:
            pprint(BAD_JOBS)
        print("check problematic jobs:")
        write_bad_job(debug)
