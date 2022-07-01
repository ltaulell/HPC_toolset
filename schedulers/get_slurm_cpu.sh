#!/bin/bash
#
# PSMN: $Id: slurm_get_cpu.sh 3686 2022-06-27 14:26:18Z ltaulell $
#

RUNNING=$(squeue -h -o "%t %C" | awk 'BEGIN {somme=0} /R/ {somme+=$2} END {print somme}')
PENDING=$(squeue -h -o "%t %C" | awk 'BEGIN {somme=0} /PD/ {somme+=$2} END {print somme}')
TOTAL=$(sinfo -h -e -o '%8X %8Y %5D' | awk 'BEGIN {somme=0} {somme+=($1 * $2 * $3)} END {print somme}')
AVAIL=$((TOTAL - RUNNING))

echo "Running Cores: ${RUNNING}"
echo "Pending Cores: ${PENDING}"
echo "Available    : ${AVAIL}"
echo "Overall Total: ${TOTAL}"

exit 0
