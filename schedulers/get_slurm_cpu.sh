#!/bin/bash
#
# PSMN: $Id: get_slurm_cpu.sh 3696 2022-07-05 12:59:50Z ltaulell $
#

# RUNNING=$(squeue -h -o "%t %C" | awk 'BEGIN {somme=0} /R/ {somme+=$2} END {print somme}')
RUNNING=$(squeue -h -o "%t %C" | awk 'BEGIN {somme=0} /R/ {somme+=($2/2)} END {print somme}')
PENDING=$(squeue -h -o "%t %C" | awk 'BEGIN {somme=0} /PD/ {somme+=$2} END {print somme}')
# TOTAL=$(sinfo -h -e -o '%8X %8Y %5D' | awk 'BEGIN {somme=0} {somme+=($1 * $2 * $3)} END {print somme}')
TOTAL=$(sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($4 / 2)} END {print somme}')
AVAIL=$(sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($2 / 2)} END {print somme}')
UNAVAIL=$(sinfo -h -d -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($4 / 2)} END {print somme}')

PERCENT=$(((RUNNING * 100) / (TOTAL-UNAVAIL)))

echo "Running Cores: ${RUNNING}"
echo "Pending Cores: ${PENDING}"
echo "Available    : ${AVAIL}"
echo "Unavailable  : ${UNAVAIL}"
echo "Overall Total: ${TOTAL}"
echo ""
echo "Overall Use  : ${PERCENT}%"


exit 0


# nb sockets, cores, nodes 'dead'
# UNAVAIL :
# sinfo -d -o '%C', divisé par %Z -> Alloc/Idle/Other/Total
# AVAIL :
# sinfo -e -o '%C', divisé par %Z -> Alloc/Idle/Other/Total

# alloc = awk -F'/' 'BEGIN {somme=0} {somme+=($1 / 2)} END {print somme}'
# avail = awk -F'/' 'BEGIN {somme=0} {somme+=($2 / 2)} END {print somme}'
# total = awk -F'/' 'BEGIN {somme=0} {somme+=($4 / 2)} END {print somme}'

# unavail = awk -F'/' 'BEGIN {somme=0} {somme+=($4 / 2)} END {print somme}'

# oneliner?
# awk -F'/' 'BEGIN {alloc=0} {avail=0} {total=0} {alloc+=($1/2)} {avail+=($2/2)} {total+=($4/2)} END {print alloc", "avail", "total}'
