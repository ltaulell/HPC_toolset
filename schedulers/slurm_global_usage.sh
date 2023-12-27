#!/bin/bash
#
# $Id: slurm_global_usage.sh 4253 2023-12-06 15:25:43Z ltaulell $
#

#
# GROS brouillon, GOTO python
#

declare -a VALUE

for i in $(sinfo -h -o "%R")
# by partitions
do

    RUNNING=$(squeue -h -p "${i}" -o "%t %C" -t R | awk 'BEGIN {somme=0} /R/ {somme+=($2)} END {print somme}')
    TOTAL=$(sinfo -h -p "${i}" -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($4)} END {print somme}')
    UNAVAIL=$(sinfo -h -p "${i}" -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($3)} END {print somme}')
    PERCENT=$(((RUNNING * 100) / (TOTAL-UNAVAIL)))
    VALUE[${i}]="${PERCENT}"
    echo ${VALUE[$i]}
done

# global
RUNNING=$(squeue -h -o "%t %C" -t R | awk 'BEGIN {somme=0} /R/ {somme+=($2)} END {print somme}')
TOTAL=$(sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($4)} END {print somme}')
UNAVAIL=$(sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($3)} END {print somme}')
PERCENT=$(((RUNNING * 100) / (TOTAL-UNAVAIL)))
GRATE="${PERCENT}"
echo $GRATE


