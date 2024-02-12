#!/bin/bash
#
# PSMN: $Id: get_slurm_cpu.sh 4082 2023-06-19 15:15:41Z ltaulell $
#

# RUNNING=$(squeue -h -o "%t %C" | awk 'BEGIN {somme=0} /R/ {somme+=$2} END {print somme}')
RUNNING=$(squeue -h -o "%t %C" | awk 'BEGIN {somme=0} /R/ {somme+=($2)} END {print somme}')
PENDING=$(squeue -h -o "%t %C" | awk 'BEGIN {somme=0} /PD/ {somme+=$2} END {print somme}')
# TOTAL=$(sinfo -h -e -o '%8X %8Y %5D' | awk 'BEGIN {somme=0} {somme+=($1 * $2 * $3)} END {print somme}')
TOTAL=$(sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($4)} END {print somme}')
AVAIL=$(sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($2)} END {print somme}')
UNAVAIL=$(sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($3)} END {print somme}')
NODES=$(sinfo -h --exact --format="%.5D")

PERCENT=$(((RUNNING * 100) / (TOTAL-UNAVAIL)))

printf "Running Cores: %5s\n" ${RUNNING}
printf "Pending Cores: %5s\n" ${PENDING}
printf "Available    : %5s\n" ${AVAIL}
printf "Unavailable  : %5s\n" ${UNAVAIL}
printf "Overall Total: %5s\n" ${TOTAL}
printf "\n"
# %% -> literal '%' symbol
printf "Overall Use  : %4s%%\n" ${PERCENT}
printf "Total nodes  : %5s\n" ${NODES}


exit 0


# nb sockets, cores, nodes 'dead'
# UNAVAIL :
# sinfo -d -o '%C', divisé par %Z -> Alloc/Idle/Other/Total
# AVAIL :
# sinfo -e -o '%C', divisé par %Z -> Alloc/Idle/Other/Total
# slurm.conf (avoid ThreadsPerCore=2, or set ThreadsPerCore=1)

# alloc = awk -F'/' 'BEGIN {somme=0} {somme+=($1 / 2)} END {print somme}'
# avail = awk -F'/' 'BEGIN {somme=0} {somme+=($2 / 2)} END {print somme}'
# total = awk -F'/' 'BEGIN {somme=0} {somme+=($4 / 2)} END {print somme}'

# unavail = awk -F'/' 'BEGIN {somme=0} {somme+=($4 / 2)} END {print somme}'

# oneliner?
# awk -F'/' 'BEGIN {alloc=0} {avail=0} {total=0} {alloc+=($1/2)} {avail+=($2/2)} {total+=($4/2)} END {print alloc", "avail", "total}'
